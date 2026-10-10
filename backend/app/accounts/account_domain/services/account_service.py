"""

Business logic for Account -- a full port of ``erpnext/accounts/doctype/account/account.py``.



Upstream lifecycle hook -> where it lives here

----------------------------------------------

``autoname``                          :meth:`AccountService._build_name`

``validate``                          :meth:`AccountService._validate` (same call order)

``validate_parent``                   :meth:`_validate_parent`

``validate_parent_child_account_type`` :meth:`_validate_parent_child_account_type`

``validate_root_details``             :meth:`_validate_root_details`

``validate_account_number``           :meth:`_validate_account_number`

``validate_disabled``                 :meth:`_validate_disabled`

``validate_group_or_ledger``          :meth:`_validate_group_or_ledger`

``set_root_and_report_type``          :meth:`_set_root_and_report_type`

``validate_mandatory``                :meth:`_validate_mandatory`

``validate_frozen_accounts_modifier`` :meth:`_validate_frozen_accounts_modifier`

``validate_balance_must_be_debit_or_credit`` :meth:`_validate_balance_must_be`

``validate_account_currency``         :meth:`_validate_account_currency`

``validate_receivable_payable_account_type`` :meth:`_warn_on_receivable_payable_change`

``validate_root_company_and_sync_account_to_children`` :meth:`_validate_root_company_and_sync`

``convert_group_to_ledger``           :meth:`convert_to_ledger`

``convert_ledger_to_group``           :meth:`convert_to_group`

``on_trash``                          :meth:`delete`

``get_account_autoname``              :func:`build_account_name`



Two upstream validations are intentionally not ported:



``validate_stock_account_type_change``

    It reads ``get_warehouse_account_map`` and ``Stock Ledger Entry``, neither

    of which exists until the Stock module is converted. It is stubbed with a

    TODO rather than silently omitted, because the guard is real and must come

    back when Stock lands.



``create_account_for_child_company``

    Multi-company mirroring. There is no Company doctype in this conversion, so

    there are no child companies to mirror into. Recorded as a TODO on

    :meth:`_validate_root_company_and_sync`.



``frappe.throw(...)`` becomes :class:`DomainValidationError`, which the API

layer renders as HTTP 400. ``frappe.msgprint`` (a warning that does not abort)

becomes a returned warning string, because there is no server-push channel here.

"""



from __future__ import annotations



import uuid

from dataclasses import dataclass, field

from typing import Optional, Protocol, Sequence



from sqlalchemy.orm import Session



from app.accounts.account_category_domain.services.account_category_service import (

    AccountCategoryService,

)

from app.accounts.account_domain.models.account import Account

from app.accounts.account_domain.repositories.account_repository import AccountRepository

from app.accounts.account_domain.schemas.account import (

    AccountCreate,

    AccountTreeNode,

    AccountUpdate,

)

from app.accounts.enums import (

    AccountType,

    BalanceMustBe,

    FreezeAccount,

    PARENT_ONLY_ACCOUNT_TYPES,

    RECEIVABLE_PAYABLE_TYPES,

    ROOT_TYPE_TO_REPORT_TYPE,

    ReportType,

    RootType,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage

from app.core.tree import TreeHelper



__all__ = [

    "AccountService",

    "GLEntryGateway",

    "CompanyDefaultsGateway",

    "NullGLEntryGateway",

    "NullCompanyDefaultsGateway",

    "build_account_name",

    "CreateOutcome",

]





# ──────────────────────────────────────────────────────────────────────────────

# Gateways: the seams where un-converted doctypes would be read

# ──────────────────────────────────────────────────────────────────────────────

class GLEntryGateway(Protocol):

    """

    Read side of GL Entry, which is not converted yet.



    Declared as a Protocol so a test can inject an in-memory double and prove

    the guard logic fires, while production wires the real repository once

    ``gl_entry_domain`` exists.

    """



    def any_entry_exists(self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID) -> bool: ...



    def any_active_entry_exists(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> bool: ...



    def get_balance(self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID) -> float: ...



    def get_entry_currency(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> Optional[str]: ...





class NullGLEntryGateway:

    """

    Stands in until ``gl_entry`` is converted.



    Reports "no entries", which makes every GL-dependent guard permissive. That

    is the correct direction to fail for a chart of accounts with no ledger yet

    -- the alternative (blocking all edits) would make the module unusable

    before the GL lands. Every method carries the TODO so the swap is findable.

    """



    # TODO(accounts-conversion): replace with GL Entry repository calls once

    # erpnext/accounts/doctype/gl_entry is converted.

    def any_entry_exists(self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID) -> bool:

        return False



    # TODO(accounts-conversion): see above; upstream filters is_cancelled == 0.

    def any_active_entry_exists(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> bool:

        return False



    # TODO(accounts-conversion): upstream calls erpnext.accounts.utils.get_balance_on.

    def get_balance(self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID) -> float:

        return 0.0



    # TODO(accounts-conversion): upstream reads GL Entry.account_currency.

    def get_entry_currency(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> Optional[str]:

        return None





class CompanyDefaultsGateway(Protocol):

    """Company default-account slots, for the "cannot disable/convert" guard."""



    def default_account_fields(self) -> dict[str, str]: ...



    def get_default_accounts(

        self, db: Session, business_id: uuid.UUID

    ) -> dict[str, Optional[str]]: ...





class NullCompanyDefaultsGateway:

    """

    No Company doctype yet, so no default-account slots to protect.



    TODO(accounts-conversion): implement against the Company domain once

    ``erpnext/setup/doctype/company`` is converted. Upstream's field list comes

    from ``get_company_default_account_fields()``.

    """



    def default_account_fields(self) -> dict[str, str]:

        return {}



    def get_default_accounts(

        self, db: Session, business_id: uuid.UUID

    ) -> dict[str, Optional[str]]:

        return {}





@dataclass

class CreateOutcome:

    """An Account plus any non-fatal warnings (``frappe.msgprint`` equivalent)."""



    account: Account

    warnings: list[str] = field(default_factory=list)





# ──────────────────────────────────────────────────────────────────────────────

# Naming -- port of get_account_autoname / get_autoname_with_number

# ──────────────────────────────────────────────────────────────────────────────

def build_account_name(

    account_number: Optional[str],

    account_name: str,

    company_abbr: Optional[str] = None,

) -> str:

    """

    Port of ``get_account_autoname``.



    Upstream::



        parts = [account_name.strip(), company.abbr]

        if cstr(account_number).strip():

            parts.insert(0, cstr(account_number).strip())

        return " - ".join(parts)



    ``company_abbr`` is optional here because there is no Company doctype; when

    it is absent the label is simply ``[number - ]name``, and the tenant scope

    keeps it unique.

    """

    name = (account_name or "").strip()

    parts = [name] + ([company_abbr.strip()] if company_abbr and company_abbr.strip() else [])

    number = (account_number or "").strip()

    if number:

        parts.insert(0, number)

    return " - ".join(parts)





# ──────────────────────────────────────────────────────────────────────────────

# Service

# ──────────────────────────────────────────────────────────────────────────────

class AccountService:

    def __init__(

        self,

        repository: Optional[AccountRepository] = None,

        *,

        gl_gateway: Optional[GLEntryGateway] = None,

        company_gateway: Optional[CompanyDefaultsGateway] = None,

        category_service: Optional[AccountCategoryService] = None,

        company_abbr: Optional[str] = None,

    ) -> None:

        self.repository = repository or AccountRepository()

        self.gl = gl_gateway or NullGLEntryGateway()

        self.company = company_gateway or NullCompanyDefaultsGateway()

        self.categories = category_service or AccountCategoryService()

        self.company_abbr = company_abbr

        #: parent_account_id is the adjacency-list parent (replaces nsm_parent_field)

        self.tree: TreeHelper[Account] = TreeHelper(Account, "parent_account_id")



    # ── helpers ──────────────────────────────────────────────────────────────

    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> Account:

        account = self.repository.get_by_id(db, business_id, account_id)

        if account is None:

            raise NotFoundError("Account", account_id)

        return account



    def _build_name(self, account_number: Optional[str], account_name: str) -> str:

        return build_account_name(account_number, account_name, self.company_abbr)



    # ── ported validators ────────────────────────────────────────────────────

    def _validate_parent(

        self, db: Session, business_id: uuid.UUID, parent_id: Optional[uuid.UUID], self_id: Optional[uuid.UUID]

    ) -> Optional[Account]:

        """

        Port of ``validate_parent``.



        Four upstream throws, in the original order: parent missing, parent is

        self, parent is a ledger, parent in another company. The company check

        is the tenant check here and is enforced by the lookup itself.

        """

        if parent_id is None:

            return None



        parent = self.repository.get_by_id(db, business_id, parent_id)

        if parent is None:

            raise DomainValidationError(

                f"Parent account {parent_id} does not exist",

                code="account_parent_not_found",

            )

        if self_id is not None and parent.id == self_id:

            raise DomainValidationError(

                "You can not assign itself as parent account",

                code="account_parent_is_self",

            )

        if not parent.is_group:

            raise DomainValidationError(

                f"Parent account {parent.account_name} can not be a ledger",

                code="account_parent_not_group",

            )

        return parent



    def _validate_parent_child_account_type(

        self, parent: Optional[Account], account_type: Optional[AccountType]

    ) -> None:

        """

        Port of ``validate_parent_child_account_type``: only the parent may

        carry these six types.

        """

        if parent is None or account_type is None:

            return

        if account_type in PARENT_ONLY_ACCOUNT_TYPES and parent.account_type == account_type:

            raise DomainValidationError(

                f"Only Parent can be of type {account_type.value}",

                code="account_type_parent_only",

            )



    def _validate_root_details(

        self, account: Account, before: Optional[Account]

    ) -> None:

        """

        Port of ``validate_root_details``.



        Two rules: an existing root cannot be edited (upstream: "Root cannot be

        edited."), and a node with no parent must be a group.

        """

        if before is not None and before.parent_account_id is None and account.parent_account_id is None:

            raise DomainValidationError(

                "Root cannot be edited.",

                code="account_root_not_editable",

            )

        if account.parent_account_id is None and not account.is_group:

            raise DomainValidationError(

                f"The root account {account.account_name} must be a group",

                code="account_root_must_be_group",

            )



    def _validate_account_number(

        self,

        db: Session,

        business_id: uuid.UUID,

        account_number: Optional[str],

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        """Port of ``validate_account_number`` -- unique per tenant."""

        if not account_number:

            return

        clash = self.repository.find_by_account_number(

            db, business_id, account_number, exclude_id=exclude_id

        )

        if clash is not None:

            raise ConflictError(

                f"Account Number {account_number} already used in account {clash.account_name}",

                code="account_number_duplicate",

                details={"account_number": account_number},

            )



    def _validate_disabled(

        self, db: Session, business_id: uuid.UUID, account: Account, before: Optional[Account]

    ) -> None:

        """Port of ``validate_disabled`` -- only fires on a change to disabled."""

        if before is None or bool(before.disabled) == bool(account.disabled):

            return

        if account.disabled:

            self._validate_default_accounts_in_company(db, business_id, account, disabling=True)



    def _validate_group_or_ledger(

        self, db: Session, business_id: uuid.UUID, account: Account, before: Optional[Account]

    ) -> None:

        """

        Port of ``validate_group_or_ledger`` -- the is_group <-> ledger guard.



        Order matters and is preserved: the GL-entry check comes first (it

        blocks conversion in *both* directions), then the group-specific and

        ledger-specific checks.

        """

        if before is None or bool(before.is_group) == bool(account.is_group):

            return



        if self.gl.any_entry_exists(db, business_id, account.id):

            raise DomainValidationError(

                "Account with existing transaction cannot be converted to ledger",

                code="account_has_gl_entries",

            )



        if account.is_group:

            # ledger -> group

            if account.account_type is not None:

                raise DomainValidationError(

                    "Cannot covert to Group because Account Type is selected.",

                    code="account_type_blocks_group",

                )

            self._validate_default_accounts_in_company(db, business_id, account, disabling=False)

        else:

            # group -> ledger

            if self.tree.has_children(db, business_id, account.id):

                raise DomainValidationError(

                    "Account with child nodes cannot be set as ledger",

                    code="account_has_children",

                )



    def _validate_default_accounts_in_company(

        self, db: Session, business_id: uuid.UUID, account: Account, *, disabling: bool

    ) -> None:

        """

        Port of ``validate_default_accounts_in_company``.



        Refuses to disable an account, or convert it to a group, when the

        tenant has nominated it as one of its default accounts. With no Company

        domain converted the slot map is empty and this passes; the shape is

        kept so wiring the gateway is a one-line change.

        """

        slots = self.company.default_account_fields()

        if not slots:

            return

        defaults = self.company.get_default_accounts(db, business_id)



        message = "Account {0} cannot be disabled as it is already set as {1}."

        if not disabling:

            message = "Account {0} cannot be converted to Group as it is already set as {1}."



        for field_name, label in slots.items():

            if defaults.get(field_name) == account.name:

                raise DomainValidationError(

                    message.format(account.name, label),

                    code="account_is_company_default",

                )



    def _set_root_and_report_type(

        self,

        db: Session,

        business_id: uuid.UUID,

        account: Account,

        parent: Optional[Account],

        before: Optional[Account],

    ) -> None:

        """

        Port of ``set_root_and_report_type`` -- the derived-classification step.



        Three behaviours, in upstream order:

        1. inherit ``report_type`` / ``root_type`` from the parent when set;

        2. if this is a group and either changed, cascade to the whole subtree;

        3. infer ``report_type`` from ``root_type`` when it is still unset.

        """

        if parent is not None:

            if parent.report_type is not None:

                account.report_type = parent.report_type

            if parent.root_type is not None:

                account.root_type = parent.root_type



        if account.is_group and before is not None:

            descendants = self.tree.get_descendants(db, business_id, account.id)

            descendant_ids = [d.id for d in descendants]



            new_root = account.root_type.value if (

                account.root_type != before.root_type and account.root_type is not None

            ) else None

            new_report = account.report_type.value if (

                account.report_type != before.report_type and account.report_type is not None

            ) else None



            if new_root is not None or new_report is not None:

                self.repository.update_subtree_classification(

                    db,

                    business_id,

                    descendant_ids,

                    root_type=new_root,

                    report_type=new_report,

                )



        if account.root_type is not None and account.report_type is None:

            account.report_type = ROOT_TYPE_TO_REPORT_TYPE[account.root_type]



    def _validate_mandatory(self, account: Account) -> None:

        """Port of ``validate_mandatory`` -- both classification fields required."""

        if account.root_type is None:

            raise DomainValidationError("Root Type is mandatory", code="root_type_mandatory")

        if account.report_type is None:

            raise DomainValidationError("Report Type is mandatory", code="report_type_mandatory")



    def _validate_frozen_accounts_modifier(

        self, account: Account, before: Optional[Account], *, actor_can_freeze: bool

    ) -> None:

        """

        Port of ``validate_frozen_accounts_modifier``.



        Upstream compares against ``Company.role_allowed_for_frozen_entries``

        and the caller's roles. Role resolution is not available here (there is

        no staff/RBAC layer yet -- the same TODO the Lead domain records), so

        the check is driven by ``actor_can_freeze``, which callers derive from

        the authenticated context. ``True`` preserves current behaviour.

        """

        if before is None or before.freeze_account == account.freeze_account:

            return

        if not actor_can_freeze:

            raise DomainValidationError(

                "You are not authorized to set Frozen value",

                code="account_freeze_not_authorized",

            )



    def _validate_balance_must_be(

        self, db: Session, business_id: uuid.UUID, account: Account, *, is_new: bool

    ) -> None:

        """

        Port of ``validate_balance_must_be_debit_or_credit``.



        Upstream skips the check for a new document (``__islocal``) and otherwise

        refuses a constraint the existing balance already contradicts.

        """

        if is_new or account.balance_must_be is None:

            return



        balance = self.gl.get_balance(db, business_id, account.id)

        if balance > 0 and account.balance_must_be == BalanceMustBe.CREDIT:

            raise DomainValidationError(

                "Account balance already in Debit, you are not allowed to set "

                "'Balance Must Be' as 'Credit'",

                code="account_balance_conflicts_debit",

            )

        if balance < 0 and account.balance_must_be == BalanceMustBe.DEBIT:

            raise DomainValidationError(

                "Account balance already in Credit, you are not allowed to set "

                "'Balance Must Be' as 'Debit'",

                code="account_balance_conflicts_credit",

            )



    def _validate_account_currency(

        self,

        db: Session,

        business_id: uuid.UUID,

        account: Account,

        *,

        is_new: bool,

        default_currency: Optional[str] = None,

    ) -> bool:

        """

        Port of ``validate_account_currency``.



        Falls back to the tenant's default currency when unset (returning

        ``False`` for "not explicitly specified", which upstream uses to decide

        what child companies inherit), then refuses a change once entries exist

        in another currency.

        """

        explicitly_specified = True

        if not account.account_currency:

            account.account_currency = default_currency

            explicitly_specified = False



        if is_new:

            return explicitly_specified



        gl_currency = self.gl.get_entry_currency(db, business_id, account.id)

        if gl_currency and account.account_currency != gl_currency:

            if self.gl.any_entry_exists(db, business_id, account.id):

                raise DomainValidationError(

                    "Currency can not be changed after making entries using some other currency",

                    code="account_currency_locked",

                )

        return explicitly_specified



    def _warn_on_receivable_payable_change(

        self, db: Session, business_id: uuid.UUID, account: Account, before: Optional[Account]

    ) -> Optional[str]:

        """

        Port of ``validate_receivable_payable_account_type``.



        Upstream this is a ``msgprint`` plus a comment -- a warning, not a

        throw. It is returned as a string so the caller can surface it instead

        of the exception machinery swallowing a non-fatal notice.

        """

        if before is None or before.account_type not in RECEIVABLE_PAYABLE_TYPES:

            return None

        if before.account_type == account.account_type:

            return None

        if self.gl.any_active_entry_exists(db, business_id, account.id):

            return (

                "There are ledger entries against this account. Changing Account Type "

                f"to non-{before.account_type.value} in live system will cause incorrect "

                f"output in 'Accounts {before.account_type.value}' report"

            )

        return None



    def _validate_stock_account_type_change(

        self, account: Account, before: Optional[Account]

    ) -> None:

        """

        Port of ``validate_stock_account_type_change`` -- STUB.



        TODO(stock-conversion): upstream blocks moving an account off

        ``account_type == "Stock"`` when Stock Ledger Entries exist against the

        warehouses mapped to it. That needs ``get_warehouse_account_map`` and

        the ``Stock Ledger Entry`` doctype, neither of which is converted yet.

        Re-implement here when Stock lands; until then the change is allowed.

        """

        return None



    def _validate_root_company_and_sync(

        self, db: Session, business_id: uuid.UUID, account: Account

    ) -> None:

        """

        Port of ``validate_root_company_and_sync_account_to_children`` -- NO-OP.



        TODO(company-conversion): upstream mirrors a new account into every

        descendant Company's chart and blocks creation in a child company

        unless the account already exists at the root. CreditBridge has no

        Company doctype -- the tenant is the scope -- so there is nothing to

        mirror. Kept as a named no-op in the validation chain so the call site

        survives and the omission is explicit rather than silent.

        """

        return None



    # ── the chain ────────────────────────────────────────────────────────────

    def _validate(

        self,

        db: Session,

        business_id: uuid.UUID,

        account: Account,

        *,

        before: Optional[Account],

        parent: Optional[Account],

        actor_can_freeze: bool = True,

        default_currency: Optional[str] = None,

    ) -> list[str]:

        """

        Port of ``Account.validate``, preserving the upstream call order.



        Returns non-fatal warnings. Raises DomainValidationError on the first

        failure, exactly as the Frappe chain aborts the save.

        """

        warnings: list[str] = []



        self._validate_parent_child_account_type(parent, account.account_type)

        self._validate_root_details(account, before)

        self._validate_account_number(

            db, business_id, account.account_number, exclude_id=account.id

        )

        self._validate_disabled(db, business_id, account, before)

        self._validate_group_or_ledger(db, business_id, account, before)

        self._set_root_and_report_type(db, business_id, account, parent, before)

        self._validate_mandatory(account)

        self._validate_frozen_accounts_modifier(

            account, before, actor_can_freeze=actor_can_freeze

        )

        self._validate_balance_must_be(

            db, business_id, account, is_new=before is None

        )

        self._validate_account_currency(

            db, business_id, account, is_new=before is None, default_currency=default_currency

        )

        self._validate_root_company_and_sync(db, business_id, account)



        receivable_warning = self._warn_on_receivable_payable_change(db, business_id, account, before)

        if receivable_warning:

            warnings.append(receivable_warning)



        self._validate_stock_account_type_change(account, before)

        return warnings



    # ── public API ───────────────────────────────────────────────────────────

    def get(self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID) -> Account:

        return self._get_or_404(db, business_id, account_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Account]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Account].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self,

        db: Session,

        business_id: uuid.UUID,

        payload: AccountCreate,

        *,

        actor_can_freeze: bool = True,

        default_currency: Optional[str] = None,

    ) -> CreateOutcome:

        warnings: list[str] = []



        parent = self._validate_parent(db, business_id, payload.parent_account_id, None)



        # ERPNext pre-fills root_type from the chosen category; mirrored here so

        # an imported COA that only carries a category still classifies.

        root_type = payload.root_type

        if root_type is None and payload.account_category:

            root_type = self.categories.root_type_for(

                db, business_id, payload.account_category

            )



        account = Account(

            business_id=business_id,

            name=self._build_name(payload.account_number, payload.account_name),

            account_name=payload.account_name,

            account_number=payload.account_number,

            parent_account_id=payload.parent_account_id,

            is_group=payload.is_group,

            root_type=root_type,

            account_type=payload.account_type,

            account_currency=payload.account_currency,

            tax_rate=payload.tax_rate,

            balance_must_be=payload.balance_must_be,

            freeze_account=payload.freeze_account,

            include_in_gross=payload.include_in_gross,

            disabled=payload.disabled,

            account_category=payload.account_category,

        )



        # Flush first: the self-FK and the subtree cascade both need an id, and

        # the GL gateways are keyed on it. Because the row is flushed before

        # validation completes, any failure below must roll back -- otherwise a

        # rejected create leaves a pending INSERT that a later commit would

        # write, and the caller's Session is left dirty.

        self.repository.add(db, account)



        try:

            warnings.extend(

                self._validate(

                    db,

                    business_id,

                    account,

                    before=None,

                    parent=parent,

                    actor_can_freeze=actor_can_freeze,

                    default_currency=default_currency,

                )

            )



            sibling = self.repository.find_by_account_name(

                db, business_id, account.account_name, parent_account_id=account.parent_account_id

            )

            if sibling is not None and sibling.id != account.id:

                raise ConflictError(

                    f"Account '{account.account_name}' already exists under the same parent",

                    code="account_duplicate_under_parent",

                )

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(account)

        return CreateOutcome(account=account, warnings=warnings)



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        account_id: uuid.UUID,

        payload: AccountUpdate,

        *,

        actor_can_freeze: bool = True,

        default_currency: Optional[str] = None,

    ) -> CreateOutcome:

        account = self._get_or_404(db, business_id, account_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return CreateOutcome(account=account)



        before = Account(

            business_id=business_id,

            name=account.name,

            account_name=account.account_name,

            account_number=account.account_number,

            parent_account_id=account.parent_account_id,

            is_group=account.is_group,

            root_type=account.root_type,

            report_type=account.report_type,

            account_type=account.account_type,

            account_currency=account.account_currency,

            balance_must_be=account.balance_must_be,

            freeze_account=account.freeze_account,

            disabled=account.disabled,

        )

        before.id = account.id



        if "parent_account_id" in changes:

            new_parent_id = changes["parent_account_id"]

            self.tree.assert_no_cycle(db, business_id, account.id, new_parent_id)

            account.parent_account_id = new_parent_id



        for field_name in (

            "account_name",

            "account_number",

            "account_type",

            "account_currency",

            "tax_rate",

            "balance_must_be",

            "freeze_account",

            "include_in_gross",

            "disabled",

            "account_category",

        ):

            if field_name in changes:

                setattr(account, field_name, changes[field_name])



        if "account_name" in changes or "account_number" in changes:

            account.name = self._build_name(account.account_number, account.account_name)



        parent = self._validate_parent(

            db, business_id, account.parent_account_id, account.id

        )



        # Same rationale as create: the row is attached and mutated before the

        # chain runs, so a rejection must not leave half-applied changes behind.

        try:

            warnings = self._validate(

                db,

                business_id,

                account,

                before=before,

                parent=parent,

                actor_can_freeze=actor_can_freeze,

                default_currency=default_currency,

            )

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(account)

        return CreateOutcome(account=account, warnings=warnings)



    def delete(self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID) -> None:

        """

        Port of ``on_trash``.



        Upstream checks GL entries and then defers to ``NestedSet.on_trash``,

        which refuses to delete a node with children. Both are enforced here.

        """

        account = self._get_or_404(db, business_id, account_id)



        if self.gl.any_entry_exists(db, business_id, account.id):

            raise DomainValidationError(

                "Account with existing transaction can not be deleted",

                code="account_has_gl_entries",

            )

        if self.tree.has_children(db, business_id, account.id):

            raise DomainValidationError(

                "Account with child nodes can not be deleted",

                code="account_has_children",

            )



        self.repository.delete(db, account)

        db.commit()



    # ── group/ledger conversion ──────────────────────────────────────────────

    def convert_to_ledger(self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID) -> Account:

        """

        Port of ``convert_group_to_ledger``.



        Note the different error strings from the generic guard -- upstream has

        both, and the messages are part of the contract users see.

        """

        account = self._get_or_404(db, business_id, account_id)



        # Upstream reaches this via `self.save()`, which re-runs

        # validate_root_details and rejects a parentless ledger. This endpoint

        # writes is_group directly, so the same rule is enforced here rather

        # than left to fall out of the save path.

        if account.parent_account_id is None:

            raise DomainValidationError(

                f"The root account {account.account_name} must be a group",

                code="account_root_must_be_group",

            )

        if self.tree.has_children(db, business_id, account.id):

            raise DomainValidationError(

                "Account with child nodes cannot be converted to ledger",

                code="account_has_children",

            )

        if self.gl.any_entry_exists(db, business_id, account.id):

            raise DomainValidationError(

                "Account with existing transaction cannot be converted to ledger",

                code="account_has_gl_entries",

            )



        account.is_group = False

        db.commit()

        db.refresh(account)

        return account



    def convert_to_group(self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID) -> Account:

        """Port of ``convert_ledger_to_group``."""

        account = self._get_or_404(db, business_id, account_id)



        if self.gl.any_entry_exists(db, business_id, account.id):

            raise DomainValidationError(

                "Account with existing transaction can not be converted to group.",

                code="account_has_gl_entries",

            )

        if account.account_type is not None:

            raise DomainValidationError(

                "Cannot convert to Group because Account Type is selected.",

                code="account_type_blocks_group",

            )



        account.is_group = True

        db.commit()

        db.refresh(account)

        return account



    # ── tree ─────────────────────────────────────────────────────────────────

    def get_tree(self, db: Session, business_id: uuid.UUID) -> tuple[list[AccountTreeNode], int]:

        """

        Materialise the tenant's whole chart as a forest.



        Replaces the Frappe tree view, which renders from ``lft``/``rgt``.

        """

        rows = self.repository.list_all(db, business_id)

        forest = self.tree.build_forest(rows)



        def convert(nodes: Sequence[object], depth: int = 0) -> list[AccountTreeNode]:

            out: list[AccountTreeNode] = []

            for node in nodes:  # type: ignore[union-attr]

                obj = node.obj  # type: ignore[attr-defined]

                out.append(

                    AccountTreeNode(

                        id=obj.id,

                        name=obj.name,

                        account_name=obj.account_name,

                        account_number=obj.account_number,

                        parent_account_id=obj.parent_account_id,

                        is_group=obj.is_group,

                        root_type=obj.root_type,

                        report_type=obj.report_type,

                        account_type=obj.account_type,

                        account_currency=obj.account_currency,

                        disabled=obj.disabled,

                        depth=depth,

                        children=convert(node.children, depth + 1),  # type: ignore[attr-defined]

                    )

                )

            return out



        return convert(forest), len(rows)



    def list_parent_options(

        self, db: Session, business_id: uuid.UUID, *, search: Optional[str] = None

    ) -> list[Account]:

        """Port of the ``get_parent_account`` query -- parent picker source."""

        return self.repository.list_groups(db, business_id, search=search)

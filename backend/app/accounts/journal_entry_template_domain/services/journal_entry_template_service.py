"""

Business logic for Journal Entry Template -- port of

``erpnext/accounts/doctype/journal_entry_template/journal_entry_template.py``.



Upstream hook -> here

-------------------

``autoname`` (``field:template_title``)   :meth:`create`

``validate``                              :meth:`_validate`

  ``validate_party``                        :meth:`_validate_party`

  ``validate_account_company``              :meth:`_validate_account_company`



``validate_account_company`` upstream compares ``Account.company`` with the

template's ``company``. ``company`` collapsed into ``business_id`` here, so the

check becomes a tenant check: resolve the row's account inside this tenant and

reject a missing or foreign one. The intent -- a template row may not reach an

account that is not this tenant's -- is unchanged.



``validate_party`` is ported in full. ``party_type`` and ``party`` stay strings

(Customer/Supplier are not converted), but the rule upstream actually enforces is

about the *combination* and the account type, both of which are available here.



``get_naming_series`` (a whitelisted helper returning Journal Entry's series

options) is not ported -- the series is exposed as ``NAMING_SERIES`` on the

journal entry model.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.enums import AccountType

from app.accounts.journal_entry_template_account_domain.models.journal_entry_template_account import (

    JournalEntryTemplateAccount,

)

from app.accounts.journal_entry_template_domain.models.journal_entry_template import (

    JournalEntryTemplate,

)

from app.accounts.journal_entry_template_domain.repositories.journal_entry_template_repository import (

    JournalEntryTemplateRepository,

)

from app.accounts.journal_entry_template_domain.schemas.journal_entry_template import (

    JournalEntryTemplateCreate,

    JournalEntryTemplateUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["JournalEntryTemplateService"]



#: Port of the list literal in ``validate_party``.

PARTY_ALLOWED_ACCOUNT_TYPES = {AccountType.RECEIVABLE, AccountType.PAYABLE}





class JournalEntryTemplateService:

    def __init__(

        self, repository: Optional[JournalEntryTemplateRepository] = None

    ) -> None:

        self.repository = repository or JournalEntryTemplateRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> JournalEntryTemplate:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Journal Entry Template", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _account_for(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> Account:

        account = db.get(Account, account_id)

        if account is None or account.business_id != business_id:

            raise DomainValidationError(

                f"Account {account_id} does not belong to this company",

                code="journal_entry_template_account_not_found",

            )

        return account



    def _validate_party(

        self, db: Session, business_id: uuid.UUID, row: JournalEntryTemplate

    ) -> None:

        """

        Port of ``validate_party``.



        A row may only name a party_type when its account is Receivable or

        Payable, and may only name a party when it also names a party_type.

        """

        for entry in row.accounts:

            if entry.account_id is None:

                continue



            if entry.party_type:

                account = self._account_for(db, business_id, entry.account_id)

                if account.account_type not in PARTY_ALLOWED_ACCOUNT_TYPES:

                    raise DomainValidationError(

                        f"Check row {entry.idx} for account {account.name}: Party Type "

                        f"is only allowed for Receivable or Payable accounts",

                        code="journal_entry_template_party_type_not_allowed",

                    )



            if entry.party and not entry.party_type:

                account = self._account_for(db, business_id, entry.account_id)

                raise DomainValidationError(

                    f"Check row {entry.idx} for account {account.name}: Party is only "

                    f"allowed if Party Type is set",

                    code="journal_entry_template_party_without_type",

                )



    def _validate_account_company(

        self, db: Session, business_id: uuid.UUID, row: JournalEntryTemplate

    ) -> None:

        """

        Port of ``validate_account_company``.



        Upstream: the row's account must belong to the template's company. Here

        that is the tenant, so resolving the account inside it is the check.

        """

        for entry in row.accounts:

            if entry.account_id is None:

                raise DomainValidationError(

                    f"Row {entry.idx}: Account is mandatory",

                    code="journal_entry_template_account_mandatory",

                )

            self._account_for(db, business_id, entry.account_id)



    def _validate(

        self, db: Session, business_id: uuid.UUID, row: JournalEntryTemplate

    ) -> None:

        # Upstream order preserved: party first, then account/company.

        self._validate_party(db, business_id, row)

        self._validate_account_company(db, business_id, row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> JournalEntryTemplate:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[JournalEntryTemplate]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[JournalEntryTemplate].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_accounts(

        self, business_id: uuid.UUID, row: JournalEntryTemplate, accounts: list[dict]

    ) -> None:

        row.accounts.clear()

        for idx, item in enumerate(accounts, start=1):

            row.accounts.append(

                JournalEntryTemplateAccount(

                    business_id=business_id,

                    idx=idx,

                    account_id=item.get("account_id"),

                    party_type=item.get("party_type"),

                    party=item.get("party"),

                    cost_center_id=item.get("cost_center_id"),

                    project=item.get("project"),

                )

            )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: JournalEntryTemplateCreate

    ) -> JournalEntryTemplate:

        name = payload.template_title.strip()

        if not name:

            raise DomainValidationError(

                "Template Title is mandatory",

                code="journal_entry_template_title_mandatory",

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Journal Entry Template '{name}' already exists",

                code="journal_entry_template_duplicate",

            )



        row = JournalEntryTemplate(

            business_id=business_id,

            name=name,

            template_title=name,

            voucher_type=payload.voucher_type,

            naming_series=payload.naming_series,

            is_opening=payload.is_opening,

            multi_currency=bool(payload.multi_currency),

        )

        self._replace_accounts(

            business_id, row, [a.model_dump() for a in payload.accounts]

        )



        try:

            db.flush()  # children need ids before validation reads them

            self._validate(db, business_id, row)

            self.repository.add(db, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        row_id: uuid.UUID,

        payload: JournalEntryTemplateUpdate,

    ) -> JournalEntryTemplate:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "accounts":

                    self._replace_accounts(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, row_id)

        self.repository.delete(db, row)

        db.commit()

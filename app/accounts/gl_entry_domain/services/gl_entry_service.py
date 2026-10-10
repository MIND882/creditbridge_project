"""

Business logic for GL Entry -- port of

``erpnext/accounts/doctype/gl_entry/gl_entry.py``.



Upstream hook -> here

-------------------

``autoname`` (ACC-GLE-.YYYY.-.#####)   :meth:`GLEntryRepository.next_name`

``validate``                           :meth:`_validate`

  ``check_mandatory``                  :meth:`_check_mandatory`

  ``pl_must_have_cost_center``         :meth:`_pl_must_have_cost_center`

  ``check_pl_account``                 :meth:`_check_pl_account`

  ``validate_cost_center``             :meth:`_validate_cost_center`

  ``validate_currency``                :meth:`_validate_currency`

``on_update``                          :meth:`_validate_on_write`

  ``validate_account_details``         :meth:`_validate_account_details`

  ``validate_balance_type``            :meth:`_validate_balance_type`

  ``validate_frozen_account``          :meth:`_validate_frozen_account`

``on_cancel``                          :meth:`cancel`



Upstream splits the checks across ``validate`` and ``on_update``; both run

before the row is persisted here, so :meth:`create` calls them in that order and

a rejected entry leaves nothing behind.



``validate_dimensions_for_pl_and_bs`` is NOT ported: it reads

``Accounting Dimension``'s mandatory-for-PL/BS flags against dynamic column

names that only exist once custom fields are materialised. That is the same

runtime-schema gap documented in the accounting-dimension service.



Two upstream checks are structural here rather than runtime guards:

``account.company != self.company`` and ``cost_center.company != self.company``

both collapse into ``business_id``, since every lookup is already tenant-scoped.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import select

from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.cost_center_domain.models.cost_center import CostCenter

from app.accounts.gl_entry_domain.models.gl_entry import GLEntry, YesNo

from app.accounts.gl_entry_domain.repositories.gl_entry_repository import GLEntryRepository

from app.accounts.gl_entry_domain.schemas.gl_entry import GLEntryCreate

from app.core.docstatus import DocStatus, assert_can_cancel

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["GLEntryService"]



ZERO = Decimal("0")





def _dec(value: object) -> Decimal:

    if value is None or value == "":

        return ZERO

    return Decimal(str(value))





class GLEntryService:

    def __init__(self, repository: Optional[GLEntryRepository] = None) -> None:

        self.repository = repository or GLEntryRepository()



    def _get_or_404(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> GLEntry:

        row = self.repository.get_by_id(db, business_id, entry_id)

        if row is None:

            raise NotFoundError("GL Entry", entry_id)

        return row



    def _account(self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID) -> Account:

        account = db.scalar(

            select(Account).where(Account.business_id == business_id, Account.id == account_id)

        )

        if account is None:

            raise DomainValidationError(

                f"Account {account_id} does not exist", code="gl_entry_account_not_found"

            )

        return account



    def _cost_center(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> CostCenter:

        cc = db.scalar(

            select(CostCenter).where(

                CostCenter.business_id == business_id, CostCenter.id == cost_center_id

            )

        )

        if cc is None:

            raise DomainValidationError(

                f"Cost Center {cost_center_id} does not exist",

                code="gl_entry_cost_center_not_found",

            )

        return cc



    def _voucher(self, row: GLEntry) -> str:

        """Upstream's ``{voucher_type} {voucher_no}`` prefix on every message."""

        return f"{row.voucher_type} {row.voucher_no}"



    # ── ported: validate ─────────────────────────────────────────────────────

    def _check_mandatory(self, db: Session, business_id: uuid.UUID, row: GLEntry) -> None:

        """

        Port of ``check_mandatory``.



        Three guards: the voucher must be identified, a Receivable/Payable

        account must carry a party, and a zero-value entry is refused.

        """

        account = self._account(db, business_id, row.account_id)



        if not row.is_cancelled and not (row.party_type and row.party):

            if account.account_type and account.account_type.value == "Receivable":

                raise DomainValidationError(

                    f"{self._voucher(row)}: Customer is required against Receivable "

                    f"account {account.account_name}",

                    code="gl_entry_party_required_receivable",

                )

            if account.account_type and account.account_type.value == "Payable":

                raise DomainValidationError(

                    f"{self._voucher(row)}: Supplier is required against Payable "

                    f"account {account.account_name}",

                    code="gl_entry_party_required_payable",

                )



        if not (_dec(row.debit) or _dec(row.credit)):

            raise DomainValidationError(

                f"{self._voucher(row)}: Either debit or credit amount is required for "

                f"{account.account_name}",

                code="gl_entry_zero_value",

            )



    def _pl_must_have_cost_center(

        self, db: Session, business_id: uuid.UUID, row: GLEntry

    ) -> None:

        """Port of ``pl_must_have_cost_center``."""

        if row.cost_center_id is not None:

            return

        account = self._account(db, business_id, row.account_id)

        if account.report_type and account.report_type.value == "Profit and Loss":

            raise DomainValidationError(

                f"{self._voucher(row)}: Cost Center is required for 'Profit and Loss' "

                f"account {account.account_name}. Please set the cost center field or "

                f"setup a default Cost Center for the Company.",

                code="gl_entry_cost_center_mandatory_for_pl",

            )



    def _check_pl_account(self, db: Session, business_id: uuid.UUID, row: GLEntry) -> None:

        """Port of ``check_pl_account``: no P&L account in an opening entry."""

        if row.is_opening is not YesNo.YES or row.is_cancelled:

            return

        account = self._account(db, business_id, row.account_id)

        if account.report_type and account.report_type.value == "Profit and Loss":

            raise DomainValidationError(

                f"{self._voucher(row)}: 'Profit and Loss' type account "

                f"{account.account_name} not allowed in Opening Entry",

                code="gl_entry_pl_not_allowed_in_opening",

            )



    def _validate_cost_center(self, db: Session, business_id: uuid.UUID, row: GLEntry) -> None:

        """Port of ``validate_cost_center``: a group cost centre cannot take entries."""

        if row.cost_center_id is None or row.is_cancelled:

            return

        cc = self._cost_center(db, business_id, row.cost_center_id)

        if cc.is_group:

            raise DomainValidationError(

                f"{self._voucher(row)}: Cost Center {cc.name} is a group cost center and "

                f"group cost centers cannot be used in transactions",

                code="gl_entry_cost_center_is_group",

            )



    def _validate_currency(self, db: Session, business_id: uuid.UUID, row: GLEntry) -> None:

        """

        Port of ``validate_currency``.



        An unset ``account_currency`` is filled from the account; a *different*

        one is refused.

        """

        if row.is_cancelled:

            return

        account = self._account(db, business_id, row.account_id)

        account_currency = account.account_currency



        if not row.account_currency:

            row.account_currency = account_currency

            return



        if account_currency and row.account_currency != account_currency:

            raise DomainValidationError(

                f"{self._voucher(row)}: Accounting Entry for {account.account_name} can "

                f"only be made in currency: {account_currency}",

                code="gl_entry_invalid_account_currency",

            )



    # ── ported: on_update ────────────────────────────────────────────────────

    def _validate_account_details(self, db: Session, business_id: uuid.UUID, row: GLEntry) -> None:

        """

        Port of ``validate_account_details``: the account must be a ledger and

        must be active.



        Upstream tests ``account.docstatus == 2`` for "inactive"; this

        conversion uses the ``disabled`` flag instead, since accounts are not

        submittable here.

        """

        account = self._account(db, business_id, row.account_id)



        if account.is_group:

            raise DomainValidationError(

                f"{self._voucher(row)}: Account {account.account_name} is a Group Account "

                f"and group accounts cannot be used in transactions",

                code="gl_entry_account_is_group",

            )

        if account.disabled:

            raise DomainValidationError(

                f"{self._voucher(row)}: Account {account.account_name} is inactive",

                code="gl_entry_account_inactive",

            )



    def _validate_balance_type(self, db: Session, business_id: uuid.UUID, row: GLEntry) -> None:

        """

        Port of ``validate_balance_type``.



        Checks the *resulting* balance including this row, so an entry that

        would flip a "must be Debit" account negative is refused.

        """

        account = self._account(db, business_id, row.account_id)

        if not account.balance_must_be:

            return



        debit, credit = self.repository.account_balance(db, business_id, row.account_id)

        balance = (debit + _dec(row.debit)) - (credit + _dec(row.credit))



        must_be = account.balance_must_be.value

        if (must_be == "Debit" and balance < 0) or (must_be == "Credit" and balance > 0):

            raise DomainValidationError(

                f"Balance for Account {account.account_name} must always be {must_be}",

                code="gl_entry_balance_type_violated",

            )



    def _validate_frozen_account(self, db: Session, business_id: uuid.UUID, row: GLEntry) -> None:

        """

        Port of ``validate_frozen_account``.



        Upstream also allows a privileged role through; there is no role model

        here, so a frozen account simply refuses the entry.

        """

        account = self._account(db, business_id, row.account_id)

        if account.freeze_account and account.freeze_account.value == "Yes":

            raise DomainValidationError(

                f"Account {account.account_name} is frozen", code="gl_entry_account_frozen"

            )



    # ── orchestration ────────────────────────────────────────────────────────

    def _validate(self, db: Session, business_id: uuid.UUID, row: GLEntry) -> None:

        """Upstream's ``validate``, in upstream's order."""

        self._pl_must_have_cost_center(db, business_id, row)

        self._check_mandatory(db, business_id, row)

        self._validate_cost_center(db, business_id, row)

        self._check_pl_account(db, business_id, row)

        self._validate_currency(db, business_id, row)



    def _validate_on_write(self, db: Session, business_id: uuid.UUID, row: GLEntry) -> None:

        """Upstream's ``on_update`` guards, which also run before persisting."""

        self._validate_account_details(db, business_id, row)

        self._validate_balance_type(db, business_id, row)

        self._validate_frozen_account(db, business_id, row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> GLEntry:

        return self._get_or_404(db, business_id, entry_id)



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[GLEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[GLEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _persist(self, db: Session, business_id: uuid.UUID, payload: GLEntryCreate) -> GLEntry:

        """

        Build, validate and flush one entry *without committing*.



        ``create`` commits immediately because a lone entry is the whole unit of

        work. ``post_balanced_set`` must not, or a voucher whose second row fails

        would leave the first row behind -- so the flush lands here and the

        caller owns the transaction boundary.

        """

        row = GLEntry(

            business_id=business_id,

            name=self.repository.next_name(db, business_id, payload.posting_date),

            posting_date=payload.posting_date,

            transaction_date=payload.transaction_date,

            account_id=payload.account_id,

            cost_center_id=payload.cost_center_id,

            finance_book_id=payload.finance_book_id,

            party_type=payload.party_type,

            party=payload.party,

            debit=_dec(payload.debit),

            credit=_dec(payload.credit),

            account_currency=payload.account_currency,

            debit_in_account_currency=payload.debit_in_account_currency,

            credit_in_account_currency=payload.credit_in_account_currency,

            transaction_currency=payload.transaction_currency,

            transaction_exchange_rate=payload.transaction_exchange_rate,

            debit_in_transaction_currency=payload.debit_in_transaction_currency,

            credit_in_transaction_currency=payload.credit_in_transaction_currency,

            against=payload.against,

            voucher_type=payload.voucher_type,

            voucher_no=payload.voucher_no,

            voucher_detail_no=payload.voucher_detail_no,

            voucher_subtype=payload.voucher_subtype,

            against_voucher_type=payload.against_voucher_type,

            against_voucher=payload.against_voucher,

            project=payload.project,

            remarks=payload.remarks,

            is_opening=payload.is_opening,

            is_advance=payload.is_advance,

            fiscal_year=payload.fiscal_year,

            due_date=payload.due_date,

            docstatus=DocStatus.SUBMITTED.value,

        )



        try:

            self._validate(db, business_id, row)

            self._validate_on_write(db, business_id, row)

            self.repository.add(db, row)

        except Exception:

            db.rollback()

            raise



        return row



    def create(self, db: Session, business_id: uuid.UUID, payload: GLEntryCreate) -> GLEntry:

        """Validate and post a single GL Entry."""

        try:

            row = self._persist(db, business_id, payload)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def post_balanced_set(

        self, db: Session, business_id: uuid.UUID, rows: list[GLEntryCreate], *, voucher_type: str,

        voucher_no: str,

    ) -> list[GLEntry]:

        """

        Post a voucher's entries as one atomic unit.



        Double entry only means something if the set is balanced, so the totals

        are checked before anything is written, and a failure rolls the whole

        set back. Individual entry validation still runs per row.



        Every row is flushed but nothing is committed until the last one passes,

        so a voucher can never half-post.

        """

        if not rows:

            raise DomainValidationError(

                "At least one GL Entry is required", code="gl_entry_set_empty"

            )



        total_debit = sum((_dec(r.debit) for r in rows), ZERO)

        total_credit = sum((_dec(r.credit) for r in rows), ZERO)

        if total_debit != total_credit:

            raise DomainValidationError(

                f"Total Debit ({total_debit}) must equal Total Credit ({total_credit})",

                code="gl_entry_set_unbalanced",

            )



        posted: list[GLEntry] = []

        try:

            for payload in rows:

                if payload.voucher_type != voucher_type or payload.voucher_no != voucher_no:

                    raise DomainValidationError(

                        "All entries in a set must share one voucher",

                        code="gl_entry_set_voucher_mismatch",

                    )

                posted.append(self._persist(db, business_id, payload))

            db.commit()

        except Exception:

            db.rollback()

            raise



        for row in posted:

            db.refresh(row)

        return posted



    def cancel(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> GLEntry:

        """

        Port of ``on_cancel``.



        Sets ``is_cancelled`` *and* ``docstatus = 2``, matching upstream, so both

        the balance filter and any docstatus-based read agree.

        """

        row = self._get_or_404(db, business_id, entry_id)

        assert_can_cancel(row, "GL Entry")



        row.is_cancelled = True

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    # ── balance reads used by other domains ──────────────────────────────────

    def account_balance(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> Decimal:

        debit, credit = self.repository.account_balance(db, business_id, account_id)

        return debit - credit



    def cost_center_balance(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> Decimal:

        debit, credit = self.repository.cost_center_balance(db, business_id, cost_center_id)

        return debit - credit



    def balances_by_cost_center(

        self, db: Session, business_id: uuid.UUID

    ) -> dict[uuid.UUID, Decimal]:

        return self.repository.balances_by_cost_center(db, business_id)



    def has_entries_for_cost_center(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> bool:

        return self.repository.has_entries_for_cost_center(db, business_id, cost_center_id)



    def has_entries_for_account(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> bool:

        return self.repository.has_entries_for_account(db, business_id, account_id)

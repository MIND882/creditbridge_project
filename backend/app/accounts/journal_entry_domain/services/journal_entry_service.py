"""

Business logic for Journal Entry -- port of

``erpnext/accounts/doctype/journal_entry/journal_entry.py``.



Upstream hook -> here

-------------------

``naming_series`` (ACC-JV-.YYYY.-)   :meth:`JournalEntryRepository.next_name`

``validate``                          :meth:`_validate`

  ``validate_empty_accounts_table``   :meth:`_validate_not_empty`

  ``validate_party``                  :meth:`_validate_party`

  ``validate_cheque_info``            :meth:`_validate_cheque_info`

  ``validate_debit_credit_amount``    :meth:`_validate_row_amounts`

  ``set_total_debit_credit``          :meth:`_set_totals`

  ``validate_total_debit_and_credit`` :meth:`_validate_balanced`

``before_submit`` / ``on_submit``     :meth:`_post_gl_entries`

``on_cancel``                         :meth:`cancel`



Upstream's ``validate`` is long and reaches into many doctypes. The steps that

need something unconverted are omitted and listed in the model docstring; the

arithmetic and party rules -- the ones that actually protect the ledger -- are

ported in full.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import select

from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.gl_entry_domain.schemas.gl_entry import GLEntryCreate

from app.accounts.gl_entry_domain.services.gl_entry_service import GLEntryService

from app.accounts.journal_entry_account_domain.models.journal_entry_account import (

    JournalEntryAccount,

)

from app.accounts.journal_entry_domain.models.journal_entry import (

    JournalEntry,

    JournalVoucherType,

    YesNo,

)

from app.accounts.journal_entry_domain.repositories.journal_entry_repository import (

    JournalEntryRepository,

)

from app.accounts.journal_entry_domain.schemas.journal_entry import (

    JournalEntryCreate,

    JournalEntryUpdate,

)

from app.accounts.fiscal_year_domain.services.fiscal_year_service import (

    FiscalYearService,

)

from app.core.docstatus import DocStatus, assert_can_cancel, assert_can_submit

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["JournalEntryService"]



ZERO = Decimal("0")





def _dec(value: object) -> Decimal:

    if value is None or value == "":

        return ZERO

    return Decimal(str(value))





class JournalEntryService:

    def __init__(

        self,

        repository: Optional[JournalEntryRepository] = None,

        *,

        gl_service: Optional[GLEntryService] = None,

    ) -> None:

        self.repository = repository or JournalEntryRepository()

        self._fiscal_years = FiscalYearService()

        self.gl = gl_service or GLEntryService()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID

    ) -> JournalEntry:

        row = self.repository.get_by_id(db, business_id, entry_id)

        if row is None:

            raise NotFoundError("Journal Entry", entry_id)

        return row



    def _account(self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID) -> Account:

        account = db.scalar(

            select(Account).where(Account.business_id == business_id, Account.id == account_id)

        )

        if account is None:

            raise DomainValidationError(

                f"Account {account_id} does not exist", code="journal_entry_account_not_found"

            )

        return account



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_not_empty(row: JournalEntry) -> None:

        """Port of ``validate_empty_accounts_table``."""

        if not row.accounts:

            raise DomainValidationError(

                "Accounts table cannot be blank.", code="journal_entry_no_rows"

            )



    def _validate_party(self, db: Session, business_id: uuid.UUID, row: JournalEntry) -> None:

        """

        Port of ``validate_party``.



        A Receivable or Payable account needs a party. The second upstream

        branch -- that the party type's own account type must agree with the

        account's -- is skipped, because it reads the Party Type doctype, which

        is not converted.

        """

        for child in row.accounts:

            account = self._account(db, business_id, child.account_id)

            if not account.account_type:

                continue

            if account.account_type.value not in ("Receivable", "Payable"):

                continue

            if not (child.party_type and child.party) and not row.party_not_required:

                raise DomainValidationError(

                    f"Row {child.idx}: Party Type and Party is required for "

                    f"Receivable / Payable account {account.account_name}",

                    code="journal_entry_party_required",

                )



    @staticmethod

    def _validate_cheque_info(row: JournalEntry) -> None:

        """

        Port of ``validate_cheque_info``.



        Upstream raises these through ``msgprint(..., raise_exception=1)``, which

        is a hard error despite the name.

        """

        if row.voucher_type in (

            JournalVoucherType.BANK_ENTRY,

            JournalVoucherType.CASH_ENTRY,

        ) and not (row.cheque_no and row.cheque_date):

            raise DomainValidationError(

                f"Reference No & Reference Date is required for {row.voucher_type.value}",

                code="journal_entry_cheque_info_missing",

            )

        if row.cheque_date and not row.cheque_no:

            raise DomainValidationError(

                "Reference No is mandatory if you entered Reference Date",

                code="journal_entry_cheque_no_mandatory",

            )



    @staticmethod

    def _validate_row_amounts(row: JournalEntry) -> None:

        """

        Port of ``validate_debit_credit_amount``.



        Exempted for a multi-currency Exchange Gain Or Loss entry, whose rows

        are rounded by the revaluation and can legitimately land on zero.

        """

        exempt = row.voucher_type is JournalVoucherType.EXCHANGE_GAIN_OR_LOSS and row.multi_currency

        if exempt:

            return

        for child in row.accounts:

            if not _dec(child.debit) and not _dec(child.credit):

                raise DomainValidationError(

                    f"Row {child.idx}: Both Debit and Credit values cannot be zero",

                    code="journal_entry_row_amount_zero",

                )



    @staticmethod

    def _set_totals(row: JournalEntry) -> None:

        """

        Port of ``set_total_debit_and_credit``.



        Also carries upstream's rule that one row cannot carry both a debit and

        a credit.

        """

        total_debit = total_credit = ZERO

        for child in row.accounts:

            if _dec(child.debit) and _dec(child.credit):

                raise DomainValidationError(

                    "You cannot credit and debit same account at the same time",

                    code="journal_entry_row_both_sides",

                )

            total_debit += _dec(child.debit)

            total_credit += _dec(child.credit)



        row.total_debit = total_debit

        row.total_credit = total_credit

        row.difference = total_debit - total_credit



    @staticmethod

    def _validate_balanced(row: JournalEntry) -> None:

        """Port of ``validate_total_debit_and_credit``."""

        exempt = row.voucher_type is JournalVoucherType.EXCHANGE_GAIN_OR_LOSS and row.multi_currency

        if exempt:

            return

        if row.difference:

            raise DomainValidationError(

                f"Total Debit must be equal to Total Credit. The difference is {row.difference}",

                code="journal_entry_unbalanced",

            )



    @staticmethod

    def _set_opening_flag(row: JournalEntry) -> None:

        """Upstream forces ``is_opening`` from the voucher type."""

        if row.voucher_type is JournalVoucherType.OPENING_ENTRY:

            row.is_opening = YesNo.YES

        elif not row.is_opening:

            row.is_opening = YesNo.NO



    @staticmethod

    def _set_against_account(row: JournalEntry) -> None:

        """

        Port of ``set_against_account``: each row's ``against_account`` becomes

        the comma-joined list of the *other* rows' accounts.

        """

        for child in row.accounts:

            others = [

                other.account.name

                for other in row.accounts

                if other.id != child.id and other.account is not None

            ]

            child.against_account = ", ".join(others) if others else None



    def _resolve_fiscal_year(

        self, db: Session, business_id: uuid.UUID, row: JournalEntry

    ) -> str:

        """

        The fiscal year covering ``posting_date``.



        Upstream ``AccountsController.validate_date_with_fiscal_year`` calls

        ``get_fiscal_year`` for doctypes without a ``fiscal_year`` field, which

        raises ``FiscalYearError`` when nothing covers the date. A journal entry

        has no such field, so the failure is a hard error.



        The resolved year is returned rather than cached on the instance: a

        service is shared across requests, so per-row state on ``self`` would

        leak between them.

        """

        fy = self._fiscal_years.get_for_date(db, business_id, row.posting_date)

        if fy is None:

            raise DomainValidationError(

                f"Posting Date {row.posting_date.isoformat()} is not in any "

                f"active Fiscal Year",

                code="journal_entry_not_in_fiscal_year",

                details={"posting_date": row.posting_date.isoformat()},

            )

        return fy.year



    def _validate(self, db: Session, business_id: uuid.UUID, row: JournalEntry) -> None:

        self._resolve_fiscal_year(db, business_id, row)

        self._set_opening_flag(row)

        self._validate_not_empty(row)

        self._validate_party(db, business_id, row)

        self._validate_cheque_info(row)

        self._validate_row_amounts(row)

        self._set_totals(row)

        self._validate_balanced(row)



    # ── GL posting ───────────────────────────────────────────────────────────

    def _gl_payloads(self, row: JournalEntry, fiscal_year: Optional[str] = None) -> list[GLEntryCreate]:

        """Build the GL Entry set this voucher posts."""

        payloads: list[GLEntryCreate] = []

        for child in row.accounts:

            payloads.append(

                GLEntryCreate(

                    posting_date=row.posting_date,

                    fiscal_year=fiscal_year,

                    account_id=child.account_id,

                    cost_center_id=child.cost_center_id,

                    debit=_dec(child.debit),

                    credit=_dec(child.credit),

                    account_currency=child.account_currency,

                    debit_in_account_currency=child.debit_in_account_currency,

                    credit_in_account_currency=child.credit_in_account_currency,

                    party_type=child.party_type,

                    party=child.party,

                    project=child.project,

                    voucher_type=JournalVoucherType.JOURNAL_ENTRY.value,

                    voucher_no=row.name,

                    voucher_detail_no=str(child.id),

                    against=child.against_account,

                    against_voucher_type=child.reference_type,

                    against_voucher=child.reference_name,

                    remarks=row.remark or row.user_remark,

                    is_opening=YesNo.YES if row.is_opening is YesNo.YES else YesNo.NO,

                )

            )

        return payloads



    def _post_gl_entries(

        self, db: Session, business_id: uuid.UUID, row: JournalEntry

    ) -> None:

        """Port of ``make_gl_entries`` on submit."""

        self.gl.post_balanced_set(

            db,

            business_id,

            self._gl_payloads(row, self._resolve_fiscal_year(db, business_id, row)),

            voucher_type=JournalVoucherType.JOURNAL_ENTRY.value,

            voucher_no=row.name,

        )



    def _reverse_gl_entries(

        self, db: Session, business_id: uuid.UUID, row: JournalEntry

    ) -> None:

        """

        Port of the reversal half of ``make_gl_entries`` on cancel.



        Cancels the entries this voucher posted rather than writing mirror rows,

        which keeps the ledger free of duplicated history while still removing

        the amounts from every balance.

        """

        for entry in self.gl.repository.list_for_voucher(

            db, business_id, JournalVoucherType.JOURNAL_ENTRY.value, row.name

        ):

            if not entry.is_cancelled:

                self.gl.cancel(db, business_id, entry.id)



    # ── public API ───────────────────────────────────────────────────────────

    def get(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> JournalEntry:

        return self._get_or_404(db, business_id, entry_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[JournalEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[JournalEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_children(

        self,

        business_id: uuid.UUID,

        row: JournalEntry,

        accounts: Optional[list[dict]],

    ) -> None:

        if accounts is None:

            return

        row.accounts.clear()

        for idx, item in enumerate(accounts, start=1):

            row.accounts.append(

                JournalEntryAccount(

                    business_id=business_id,

                    idx=idx,

                    account_id=item["account_id"],

                    account_type=item.get("account_type"),

                    cost_center_id=item.get("cost_center_id"),

                    party_type=item.get("party_type"),

                    party=item.get("party"),

                    account_currency=item.get("account_currency"),

                    exchange_rate=item.get("exchange_rate"),

                    debit_in_account_currency=item.get("debit_in_account_currency"),

                    debit=item.get("debit"),

                    credit_in_account_currency=item.get("credit_in_account_currency"),

                    credit=item.get("credit"),

                    reference_type=item.get("reference_type"),

                    reference_name=item.get("reference_name"),

                    reference_due_date=item.get("reference_due_date"),

                    project=item.get("project"),

                    is_advance=item.get("is_advance"),

                    user_remark=item.get("user_remark"),

                    bank_account_id=item.get("bank_account_id"),

                    reference_detail_no=item.get("reference_detail_no"),

                )

            )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: JournalEntryCreate

    ) -> JournalEntry:

        row = JournalEntry(

            business_id=business_id,

            name=self.repository.next_name(db, business_id, payload.posting_date),

            naming_series=payload.naming_series,

            title=payload.title,

            voucher_type=payload.voucher_type,

            posting_date=payload.posting_date,

            cheque_no=payload.cheque_no,

            cheque_date=payload.cheque_date,

            user_remark=payload.user_remark,

            bill_no=payload.bill_no,

            bill_date=payload.bill_date,

            due_date=payload.due_date,

            multi_currency=payload.multi_currency,

            pay_to_recd_from=payload.pay_to_recd_from,

            mode_of_payment=payload.mode_of_payment,

            is_opening=payload.is_opening,

            write_off_based_on=payload.write_off_based_on,

            write_off_amount=payload.write_off_amount,

            party_not_required=payload.party_not_required,

            custom_remark=payload.custom_remark,

            apply_tds=payload.apply_tds,

            docstatus=DocStatus.DRAFT.value,

        )

        self._replace_children(business_id, row, [a.model_dump() for a in payload.accounts])



        try:

            self._validate(db, business_id, row)

            self.repository.add(db, row)

            # Needs the child ids, so it runs after the first flush.

            self._set_against_account(row)

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

        entry_id: uuid.UUID,

        payload: JournalEntryUpdate,

    ) -> JournalEntry:

        row = self._get_or_404(db, business_id, entry_id)

        if not row.is_draft:

            raise DomainValidationError(

                "Only a draft Journal Entry can be edited. Cancel and re-post instead.",

                code="journal_entry_not_editable",

            )



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "accounts":

                    self._replace_children(business_id, row, value)

                else:

                    setattr(row, field_name, value)



            self._validate(db, business_id, row)

            db.flush()

            self._set_against_account(row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, entry_id)

        if not row.is_draft:

            raise DomainValidationError(

                "Only a draft Journal Entry can be deleted. Cancel it first.",

                code="journal_entry_not_deletable",

            )

        self.repository.delete(db, row)

        db.commit()



    # ── lifecycle ────────────────────────────────────────────────────────────

    def submit(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> JournalEntry:

        """Validates, posts the GL set, then flips docstatus."""

        row = self._get_or_404(db, business_id, entry_id)

        assert_can_submit(row, "Journal Entry")



        try:

            self._validate(db, business_id, row)

            db.flush()

            self._set_against_account(row)

            self._post_gl_entries(db, business_id, row)

            row.docstatus = DocStatus.SUBMITTED.value

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def cancel(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> JournalEntry:

        """Port of ``on_cancel``: reverse the GL Entries, then cancel."""

        row = self._get_or_404(db, business_id, entry_id)

        assert_can_cancel(row, "Journal Entry")



        try:

            self._reverse_gl_entries(db, business_id, row)

            row.docstatus = DocStatus.CANCELLED.value

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row

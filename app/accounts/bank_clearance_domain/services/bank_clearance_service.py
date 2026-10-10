"""

Business logic for Bank Clearance -- port of

``erpnext/accounts/doctype/bank_clearance/bank_clearance.py``.



Upstream hook -> here

-------------------

``get_payment_entries``     :meth:`get_payment_entries` (entry fetch stubbed)

``update_clearance_date``   :meth:`update_clearance_date`



Bank Clearance is a *tool*, not a ledger document: it lists unreconciled

payment entries against a bank account for a date range and stamps clearance

dates onto them.



Two upstream steps reach into doctypes that are not converted yet, and both are

stubbed as named fail-open methods rather than dropped:



* ``get_payment_entries_for_bank_clearance`` reads GL Entry / Payment Entry to

  build the list -- :meth:`fetch_candidate_entries` returns nothing, so a run

  produces an empty list rather than an error.

* The write half of ``update_clearance_date`` calls ``db_set`` on Payment Entry

  / Sales Invoice Payment -- :meth:`apply_clearance_dates` records the dates on

  the child rows only.



Upstream reports bad rows with ``msgprint`` (an interactive warning) rather than

``frappe.throw``. There is no message channel in an API, so those become 400s

with the offending row numbers in the message.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_clearance_detail_domain.models.bank_clearance_detail import (

    BankClearanceDetail,

)

from app.accounts.bank_clearance_domain.models.bank_clearance import BankClearance

from app.accounts.bank_clearance_domain.repositories.bank_clearance_repository import (

    BankClearanceRepository,

)

from app.accounts.bank_clearance_domain.schemas.bank_clearance import (

    BankClearanceCreate,

    BankClearanceUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankClearanceService"]





class BankClearanceService:

    def __init__(self, repository: Optional[BankClearanceRepository] = None) -> None:

        self.repository = repository or BankClearanceRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, clearance_id: uuid.UUID

    ) -> BankClearance:

        row = self.repository.get_by_id(db, business_id, clearance_id)

        if row is None:

            raise NotFoundError("Bank Clearance", clearance_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_dates(row: BankClearance) -> None:

        """

        ``if not (self.from_date and self.to_date)`` -> "From Date and To Date

        are Mandatory". Both are NOT NULL columns here, so the reachable case is

        a reversed range, which can only return nothing.

        """

        if not (row.from_date and row.to_date):

            raise DomainValidationError(

                "From Date and To Date are Mandatory",

                code="bank_clearance_dates_mandatory",

            )

        if row.to_date < row.from_date:

            raise DomainValidationError(

                "To Date cannot be before From Date", code="bank_clearance_dates_reversed"

            )



    @staticmethod

    def _validate_row_dates(row: BankClearance) -> None:

        """

        Port of the ``validate_entry`` closure in ``update_clearance_date``.



        Collects *all* offending rows before failing, so one response tells the

        user everything to fix rather than one row at a time.

        """

        invalid_document: list[str] = []

        invalid_cheque_date: list[str] = []



        for child in row.payment_entries:

            if not child.payment_document:

                invalid_document.append(str(child.idx))

            if (

                child.clearance_date

                and child.cheque_date

                and child.clearance_date < child.cheque_date

            ):

                invalid_cheque_date.append(str(child.idx))



        if invalid_document or invalid_cheque_date:

            parts: list[str] = []

            if invalid_document:

                parts.append(

                    f"Payment document required for row(s): {', '.join(invalid_document)}"

                )

            if invalid_cheque_date:

                parts.append(

                    "Clearance date must be after cheque date for row(s): "

                    f"{', '.join(invalid_cheque_date)}"

                )

            raise DomainValidationError(

                "Please correct the following row(s): " + " ".join(parts),

                code="bank_clearance_invalid_rows",

            )



    # ── stubbed integrations ─────────────────────────────────────────────────

    def fetch_candidate_entries(

        self, db: Session, business_id: uuid.UUID, row: BankClearance

    ) -> list[dict]:

        """

        Port of the ``get_payment_entries_for_bank_clearance`` hook -- STUB.



        TODO(accounts-conversion): upstream collects unreconciled Payment Entry

        / Journal Entry / Sales Invoice Payment rows against the account for the

        date range, then sorts by posting date. GL Entry and Payment Entry are

        not converted yet, so this returns nothing. Fail-open: the run succeeds

        with an empty list instead of erroring out.

        """

        return []



    def apply_clearance_dates(

        self, db: Session, business_id: uuid.UUID, row: BankClearance

    ) -> int:

        """

        Port of the write half of ``update_clearance_date`` -- STUB.



        TODO(accounts-conversion): upstream calls ``db_set("clearance_date", …)``

        on each linked voucher (and on Sales Invoice Payment rows) and adds a

        comment recording the change. Neither Payment Entry nor Sales Invoice is

        converted, so the clearance dates live only on the child rows here.

        Returns how many rows carried a clearance date, so the caller can report

        "nothing to update" the way upstream's ``Clearance Date not mentioned``

        message does.

        """

        return sum(1 for child in row.payment_entries if child.clearance_date)



    # ── public API ───────────────────────────────────────────────────────────

    def get(self, db: Session, business_id: uuid.UUID, clearance_id: uuid.UUID) -> BankClearance:

        return self._get_or_404(db, business_id, clearance_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BankClearance]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankClearance].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_children(

        self,

        business_id: uuid.UUID,

        row: BankClearance,

        entries: Optional[list[dict]],

    ) -> None:

        if entries is None:

            return

        row.payment_entries.clear()

        for idx, item in enumerate(entries, start=1):

            row.payment_entries.append(

                BankClearanceDetail(

                    business_id=business_id,

                    idx=idx,

                    payment_document=item.get("payment_document"),

                    payment_entry=item.get("payment_entry"),

                    against_account=item.get("against_account"),

                    amount=item.get("amount"),

                    posting_date=item.get("posting_date"),

                    cheque_number=item.get("cheque_number"),

                    cheque_date=item.get("cheque_date"),

                    clearance_date=item.get("clearance_date"),

                )

            )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BankClearanceCreate

    ) -> BankClearance:

        row = BankClearance(

            business_id=business_id,

            name=self.repository.next_name(db, business_id),

            account_id=payload.account_id,

            account_currency=payload.account_currency,

            from_date=payload.from_date,

            to_date=payload.to_date,

            bank_account_id=payload.bank_account_id,

            include_reconciled_entries=payload.include_reconciled_entries,

            include_pos_transactions=payload.include_pos_transactions,

        )

        self._replace_children(

            business_id, row, [p.model_dump() for p in payload.payment_entries]

        )



        try:

            self._validate_dates(row)

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

        clearance_id: uuid.UUID,

        payload: BankClearanceUpdate,

    ) -> BankClearance:

        row = self._get_or_404(db, business_id, clearance_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "payment_entries":

                    self._replace_children(business_id, row, value)

                else:

                    setattr(row, field_name, value)

            self._validate_dates(row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, clearance_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, clearance_id)

        self.repository.delete(db, row)

        db.commit()



    # ── the two tool actions ─────────────────────────────────────────────────

    def get_payment_entries(

        self, db: Session, business_id: uuid.UUID, clearance_id: uuid.UUID

    ) -> BankClearance:

        """

        Port of ``get_payment_entries``: re-fetch the candidate entries for the

        run's date range and replace the child rows.



        The fetch is stubbed (see :meth:`fetch_candidate_entries`), so this

        currently clears the rows and leaves them empty rather than erroring.

        """

        row = self._get_or_404(db, business_id, clearance_id)



        try:

            self._validate_dates(row)

            entries = sorted(

                self.fetch_candidate_entries(db, business_id, row),

                key=lambda entry: entry.get("posting_date"),

            )



            row.payment_entries.clear()

            for idx, entry in enumerate(entries, start=1):

                debit = entry.get("debit") or 0

                credit = entry.get("credit") or 0

                # Upstream renders `amount` as a formatted "1,000.00 Dr/Cr" string.

                amount = debit - credit

                row.payment_entries.append(

                    BankClearanceDetail(

                        business_id=business_id,

                        idx=idx,

                        payment_document=entry.get("payment_document"),

                        payment_entry=entry.get("payment_entry"),

                        against_account=entry.get("against_account"),

                        amount=f"{abs(amount)} {'Dr' if amount > 0 else 'Cr'}",

                        posting_date=entry.get("posting_date"),

                        cheque_number=entry.get("cheque_number"),

                        cheque_date=entry.get("cheque_date"),

                    )

                )

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update_clearance_date(

        self, db: Session, business_id: uuid.UUID, clearance_id: uuid.UUID

    ) -> tuple[BankClearance, int]:

        """

        Port of ``update_clearance_date``.



        Validates every row first (so one call reports every problem), then

        applies the dates. Rows with no clearance date are only pushed when

        ``include_reconciled_entries`` is set -- otherwise they would clear a

        date the user never touched.

        """

        row = self._get_or_404(db, business_id, clearance_id)



        try:

            self._validate_row_dates(row)



            if not row.include_reconciled_entries:

                pending = [c for c in row.payment_entries if c.clearance_date]

            else:

                pending = list(row.payment_entries)



            if not pending:

                # Upstream's "Clearance Date not mentioned" msgprint.

                raise DomainValidationError(

                    "Clearance Date not mentioned",

                    code="bank_clearance_no_dates_mentioned",

                )



            updated = self.apply_clearance_dates(db, business_id, row)

            # Upstream re-fetches after updating, so the list reflects reality.

            self.get_payment_entries(db, business_id, clearance_id)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row, updated

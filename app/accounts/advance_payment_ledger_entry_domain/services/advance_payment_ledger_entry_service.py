# HAND-WRITTEN

"""

Business logic for Advance Payment Ledger Entry -- port of

``erpnext/accounts/doctype/advance_payment_ledger_entry/advance_payment_ledger_entry.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    on_update



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.advance_payment_ledger_entry_domain.models.advance_payment_ledger_entry import AdvancePaymentLedgerEntry

from app.accounts.advance_payment_ledger_entry_domain.repositories.advance_payment_ledger_entry_repository import (

    AdvancePaymentLedgerEntryRepository,

)

from app.accounts.advance_payment_ledger_entry_domain.schemas.advance_payment_ledger_entry import (

    AdvancePaymentLedgerEntryCreate,

    AdvancePaymentLedgerEntryUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["AdvancePaymentLedgerEntryService"]





class AdvancePaymentLedgerEntryService:

    def __init__(self, repository: Optional[AdvancePaymentLedgerEntryRepository] = None) -> None:

        self.repository = repository or AdvancePaymentLedgerEntryRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> AdvancePaymentLedgerEntry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Advance Payment Ledger Entry", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: AdvancePaymentLedgerEntry

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> AdvancePaymentLedgerEntry:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[AdvancePaymentLedgerEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[AdvancePaymentLedgerEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(AdvancePaymentLedgerEntry).where(

                    AdvancePaymentLedgerEntry.business_id == business_id

                )

            )

            or 0

        )

        return f"ADV-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: AdvancePaymentLedgerEntryCreate

    ) -> AdvancePaymentLedgerEntry:

        row = AdvancePaymentLedgerEntry(

            business_id=business_id,

            name=self.next_name(db, business_id),

            voucher_type=payload.voucher_type,

            voucher_no=payload.voucher_no,

            against_voucher_type=payload.against_voucher_type,

            against_voucher_no=payload.against_voucher_no,

            amount=payload.amount,

            currency=payload.currency,

            event=payload.event,

            delinked=payload.delinked,

            base_amount=payload.base_amount,

            exchange_rate=payload.exchange_rate,

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

        payload: AdvancePaymentLedgerEntryUpdate,

    ) -> AdvancePaymentLedgerEntry:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> AdvancePaymentLedgerEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Advance Payment Ledger Entry")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> AdvancePaymentLedgerEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Advance Payment Ledger Entry")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

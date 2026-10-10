"""Business logic for Stock Ledger Entry -- port of

``erpnext/stock/doctype/stock_ledger_entry/stock_ledger_entry.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 9 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_ledger_entry_domain.models.stock_ledger_entry import StockLedgerEntry

from app.stock.stock_ledger_entry_domain.repositories.stock_ledger_entry_repository import (

    StockLedgerEntryRepository,

)

from app.stock.stock_ledger_entry_domain.schemas.stock_ledger_entry import (

    StockLedgerEntryCreate,

    StockLedgerEntryUpdate,

)

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["StockLedgerEntryService"]





class StockLedgerEntryService:

    def __init__(self, repository: Optional[StockLedgerEntryRepository] = None) -> None:

        self.repository = repository or StockLedgerEntryRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockLedgerEntry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Stock Ledger Entry", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: StockLedgerEntry

    ) -> None:

        """

        Upstream has 9 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockLedgerEntry:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[StockLedgerEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[StockLedgerEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``MAT-SLE-.YYYY.-.#####``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(StockLedgerEntry).where(

                    StockLedgerEntry.business_id == business_id

                )

            )

            or 0

        )

        return f"MAT-SLE-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: StockLedgerEntryCreate

    ) -> StockLedgerEntry:

        row = StockLedgerEntry(

            business_id=business_id,

            name=self.next_name(db, business_id),

            item_code_id=payload.item_code_id,

            serial_no=payload.serial_no,

            batch_no=payload.batch_no,

            warehouse_id=payload.warehouse_id,

            posting_date=payload.posting_date,

            posting_time=payload.posting_time,

            voucher_type=payload.voucher_type,

            voucher_no=payload.voucher_no,

            voucher_detail_no=payload.voucher_detail_no,

            actual_qty=payload.actual_qty,

            incoming_rate=payload.incoming_rate,

            outgoing_rate=payload.outgoing_rate,

            stock_uom_id=payload.stock_uom_id,

            qty_after_transaction=payload.qty_after_transaction,

            valuation_rate=payload.valuation_rate,

            stock_value=payload.stock_value,

            stock_value_difference=payload.stock_value_difference,

            stock_queue=payload.stock_queue,

            project=payload.project,

            company=payload.company,

            fiscal_year=payload.fiscal_year,

            is_cancelled=payload.is_cancelled,

            to_rename=payload.to_rename,

            dependant_sle_voucher_detail_no=payload.dependant_sle_voucher_detail_no,

            recalculate_rate=payload.recalculate_rate,

            serial_and_batch_bundle_id=payload.serial_and_batch_bundle_id,

            has_batch_no=payload.has_batch_no,

            has_serial_no=payload.has_serial_no,

            is_adjustment_entry=payload.is_adjustment_entry,

            auto_created_serial_and_batch_bundle=payload.auto_created_serial_and_batch_bundle,

            posting_datetime=payload.posting_datetime,

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

        payload: StockLedgerEntryUpdate,

    ) -> StockLedgerEntry:

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

    ) -> StockLedgerEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Stock Ledger Entry")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockLedgerEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Stock Ledger Entry")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

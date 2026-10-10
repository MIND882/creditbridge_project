"""Business logic for Stock Reservation Entry -- port of

``erpnext/stock/doctype/stock_reservation_entry/stock_reservation_entry.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 23 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_reservation_entry_domain.models.stock_reservation_entry import StockReservationEntry

from app.stock.stock_reservation_entry_domain.repositories.stock_reservation_entry_repository import (

    StockReservationEntryRepository,

)

from app.stock.stock_reservation_entry_domain.schemas.stock_reservation_entry import (

    StockReservationEntryCreate,

    StockReservationEntryUpdate,

)

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["StockReservationEntryService"]





class StockReservationEntryService:

    def __init__(self, repository: Optional[StockReservationEntryRepository] = None) -> None:

        self.repository = repository or StockReservationEntryRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockReservationEntry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Stock Reservation Entry", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: StockReservationEntry

    ) -> None:

        """

        Upstream has 23 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockReservationEntry:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[StockReservationEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[StockReservationEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``MAT-SRE-.YYYY.-.#####``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(StockReservationEntry).where(

                    StockReservationEntry.business_id == business_id

                )

            )

            or 0

        )

        return f"MAT-SRE-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: StockReservationEntryCreate

    ) -> StockReservationEntry:

        row = StockReservationEntry(

            business_id=business_id,

            name=self.next_name(db, business_id),

            item_code_id=payload.item_code_id,

            warehouse_id=payload.warehouse_id,

            voucher_type=payload.voucher_type,

            voucher_no=payload.voucher_no,

            voucher_detail_no=payload.voucher_detail_no,

            stock_uom_id=payload.stock_uom_id,

            project=payload.project,

            company=payload.company,

            reserved_qty=payload.reserved_qty,

            status=payload.status,

            delivered_qty=payload.delivered_qty,

            amended_from_id=payload.amended_from_id,

            available_qty=payload.available_qty,

            voucher_qty=payload.voucher_qty,

            has_serial_no=payload.has_serial_no,

            has_batch_no=payload.has_batch_no,

            reservation_based_on=payload.reservation_based_on,

            from_voucher_type=payload.from_voucher_type,

            from_voucher_detail_no=payload.from_voucher_detail_no,

            from_voucher_no=payload.from_voucher_no,

            consumed_qty=payload.consumed_qty,

            transferred_qty=payload.transferred_qty,

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

        payload: StockReservationEntryUpdate,

    ) -> StockReservationEntry:

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

    ) -> StockReservationEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Stock Reservation Entry")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockReservationEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Stock Reservation Entry")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

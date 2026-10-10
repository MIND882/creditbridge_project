"""Business logic for Stock Closing Balance -- port of

``erpnext/stock/doctype/stock_closing_balance/stock_closing_balance.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_closing_balance_domain.models.stock_closing_balance import StockClosingBalance

from app.stock.stock_closing_balance_domain.repositories.stock_closing_balance_repository import (

    StockClosingBalanceRepository,

)

from app.stock.stock_closing_balance_domain.schemas.stock_closing_balance import (

    StockClosingBalanceCreate,

    StockClosingBalanceUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["StockClosingBalanceService"]





class StockClosingBalanceService:

    def __init__(self, repository: Optional[StockClosingBalanceRepository] = None) -> None:

        self.repository = repository or StockClosingBalanceRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockClosingBalance:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Stock Closing Balance", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: StockClosingBalance

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockClosingBalance:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[StockClosingBalance]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[StockClosingBalance].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(StockClosingBalance).where(

                    StockClosingBalance.business_id == business_id

                )

            )

            or 0

        )

        return f"STO-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: StockClosingBalanceCreate

    ) -> StockClosingBalance:

        row = StockClosingBalance(

            business_id=business_id,

            name=self.next_name(db, business_id),

            item_code_id=payload.item_code_id,

            warehouse_id=payload.warehouse_id,

            posting_date=payload.posting_date,

            posting_time=payload.posting_time,

            posting_datetime=payload.posting_datetime,

            actual_qty=payload.actual_qty,

            valuation_rate=payload.valuation_rate,

            stock_value=payload.stock_value,

            company=payload.company,

            stock_uom_id=payload.stock_uom_id,

            stock_value_difference=payload.stock_value_difference,

            item_name=payload.item_name,

            item_group_id=payload.item_group_id,

            stock_closing_entry_id=payload.stock_closing_entry_id,

            inventory_dimension_key=payload.inventory_dimension_key,

            batch_no_id=payload.batch_no_id,

            fifo_queue=payload.fifo_queue,

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

        payload: StockClosingBalanceUpdate,

    ) -> StockClosingBalance:

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

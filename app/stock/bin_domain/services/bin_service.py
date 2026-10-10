"""Business logic for Bin -- port of

``erpnext/stock/doctype/bin/bin.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.bin_domain.models.bin import Bin

from app.stock.bin_domain.repositories.bin_repository import (

    BinRepository,

)

from app.stock.bin_domain.schemas.bin import (

    BinCreate,

    BinUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BinService"]





class BinService:

    def __init__(self, repository: Optional[BinRepository] = None) -> None:

        self.repository = repository or BinRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Bin:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Bin", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Bin

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Bin:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Bin]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Bin].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BinCreate

    ) -> Bin:

        row = Bin(

            business_id=business_id,

            warehouse_id=payload.warehouse_id,

            item_code_id=payload.item_code_id,

            reserved_qty=payload.reserved_qty,

            actual_qty=payload.actual_qty,

            ordered_qty=payload.ordered_qty,

            indented_qty=payload.indented_qty,

            planned_qty=payload.planned_qty,

            projected_qty=payload.projected_qty,

            reserved_qty_for_production=payload.reserved_qty_for_production,

            reserved_qty_for_sub_contract=payload.reserved_qty_for_sub_contract,

            stock_uom_id=payload.stock_uom_id,

            company=payload.company,

            valuation_rate=payload.valuation_rate,

            stock_value=payload.stock_value,

            reserved_qty_for_production_plan=payload.reserved_qty_for_production_plan,

            reserved_stock=payload.reserved_stock,

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

        payload: BinUpdate,

    ) -> Bin:

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

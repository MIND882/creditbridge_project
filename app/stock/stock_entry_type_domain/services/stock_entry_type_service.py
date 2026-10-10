"""Business logic for Stock Entry Type -- port of

``erpnext/stock/doctype/stock_entry_type/stock_entry_type.py``.



Upstream has 2 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_entry_type_domain.models.stock_entry_type import StockEntryType

from app.stock.stock_entry_type_domain.repositories.stock_entry_type_repository import (

    StockEntryTypeRepository,

)

from app.stock.stock_entry_type_domain.schemas.stock_entry_type import (

    StockEntryTypeCreate,

    StockEntryTypeUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["StockEntryTypeService"]





class StockEntryTypeService:

    def __init__(self, repository: Optional[StockEntryTypeRepository] = None) -> None:

        self.repository = repository or StockEntryTypeRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockEntryType:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Stock Entry Type", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: StockEntryType

    ) -> None:

        """

        Upstream has 2 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockEntryType:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[StockEntryType]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[StockEntryType].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: StockEntryTypeCreate

    ) -> StockEntryType:

        row = StockEntryType(

            business_id=business_id,

            name=payload.name,

            purpose=payload.purpose,

            add_to_transit=payload.add_to_transit,

            is_standard=payload.is_standard,

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

        payload: StockEntryTypeUpdate,

    ) -> StockEntryType:

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

"""Data access for StockEntryType. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_entry_type_domain.models.stock_entry_type import StockEntryType

from app.core.pagination import normalise_paging



__all__ = ["StockEntryTypeRepository"]





class StockEntryTypeRepository:

    model = StockEntryType





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[StockEntryType]:

        return db.scalar(

            select(StockEntryType).where(

                StockEntryType.business_id == business_id, StockEntryType.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[StockEntryType]:

        return db.scalar(

            select(StockEntryType).where(

                StockEntryType.business_id == business_id, StockEntryType.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[StockEntryType], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [StockEntryType.business_id == business_id]

        if search:

            conditions.append(StockEntryType.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(StockEntryType).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(StockEntryType)

            .where(*conditions)

            .order_by(StockEntryType.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: StockEntryType) -> StockEntryType:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: StockEntryType) -> None:

        db.delete(row)

        db.flush()

"""Data access for InventoryDimension. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.inventory_dimension_domain.models.inventory_dimension import InventoryDimension

from app.core.pagination import normalise_paging



__all__ = ["InventoryDimensionRepository"]





class InventoryDimensionRepository:

    model = InventoryDimension





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[InventoryDimension]:

        return db.scalar(

            select(InventoryDimension).where(

                InventoryDimension.business_id == business_id, InventoryDimension.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[InventoryDimension]:

        return db.scalar(

            select(InventoryDimension).where(

                InventoryDimension.business_id == business_id, InventoryDimension.name == name

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

    ) -> tuple[Sequence[InventoryDimension], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [InventoryDimension.business_id == business_id]

        if search:

            conditions.append(InventoryDimension.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(InventoryDimension).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(InventoryDimension)

            .where(*conditions)

            .order_by(InventoryDimension.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: InventoryDimension) -> InventoryDimension:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: InventoryDimension) -> None:

        db.delete(row)

        db.flush()

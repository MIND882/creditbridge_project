"""Data access for Warehouse. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.warehouse_domain.models.warehouse import Warehouse

from app.core.pagination import normalise_paging



__all__ = ["WarehouseRepository"]





class WarehouseRepository:

    model = Warehouse





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Warehouse]:

        return db.scalar(

            select(Warehouse).where(

                Warehouse.business_id == business_id, Warehouse.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Warehouse]:

        return db.scalar(

            select(Warehouse).where(

                Warehouse.business_id == business_id, Warehouse.name == name

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

    ) -> tuple[Sequence[Warehouse], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Warehouse.business_id == business_id]

        if search:

            conditions.append(Warehouse.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Warehouse).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Warehouse)

            .where(*conditions)

            .order_by(Warehouse.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Warehouse) -> Warehouse:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Warehouse) -> None:

        db.delete(row)

        db.flush()

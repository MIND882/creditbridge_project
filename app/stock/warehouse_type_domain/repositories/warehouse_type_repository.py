"""Data access for WarehouseType. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.warehouse_type_domain.models.warehouse_type import WarehouseType

from app.core.pagination import normalise_paging



__all__ = ["WarehouseTypeRepository"]





class WarehouseTypeRepository:

    model = WarehouseType





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[WarehouseType]:

        return db.scalar(

            select(WarehouseType).where(

                WarehouseType.business_id == business_id, WarehouseType.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[WarehouseType]:

        return db.scalar(

            select(WarehouseType).where(

                WarehouseType.business_id == business_id, WarehouseType.name == name

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

    ) -> tuple[Sequence[WarehouseType], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [WarehouseType.business_id == business_id]

        if search:

            conditions.append(WarehouseType.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(WarehouseType).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(WarehouseType)

            .where(*conditions)

            .order_by(WarehouseType.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: WarehouseType) -> WarehouseType:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: WarehouseType) -> None:

        db.delete(row)

        db.flush()

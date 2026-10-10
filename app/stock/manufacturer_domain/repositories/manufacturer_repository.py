"""Data access for Manufacturer. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.manufacturer_domain.models.manufacturer import Manufacturer

from app.core.pagination import normalise_paging



__all__ = ["ManufacturerRepository"]





class ManufacturerRepository:

    model = Manufacturer





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Manufacturer]:

        return db.scalar(

            select(Manufacturer).where(

                Manufacturer.business_id == business_id, Manufacturer.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Manufacturer]:

        return db.scalar(

            select(Manufacturer).where(

                Manufacturer.business_id == business_id, Manufacturer.name == name

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

    ) -> tuple[Sequence[Manufacturer], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Manufacturer.business_id == business_id]

        if search:

            conditions.append(Manufacturer.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Manufacturer).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Manufacturer)

            .where(*conditions)

            .order_by(Manufacturer.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Manufacturer) -> Manufacturer:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Manufacturer) -> None:

        db.delete(row)

        db.flush()

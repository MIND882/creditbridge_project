"""Data access for Uom. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.uom_domain.models.uom import Uom

from app.core.pagination import normalise_paging



__all__ = ["UomRepository"]





class UomRepository:

    model = Uom





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Uom]:

        return db.scalar(

            select(Uom).where(

                Uom.business_id == business_id, Uom.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Uom]:

        return db.scalar(

            select(Uom).where(

                Uom.business_id == business_id, Uom.name == name

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

    ) -> tuple[Sequence[Uom], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Uom.business_id == business_id]

        if search:

            conditions.append(Uom.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Uom).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Uom)

            .where(*conditions)

            .order_by(Uom.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Uom) -> Uom:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Uom) -> None:

        db.delete(row)

        db.flush()

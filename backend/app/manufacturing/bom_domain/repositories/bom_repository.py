"""Data access for Bom. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_domain.models.bom import Bom

from app.core.pagination import normalise_paging



__all__ = ["BomRepository"]





class BomRepository:

    model = Bom





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Bom]:

        return db.scalar(

            select(Bom).where(

                Bom.business_id == business_id, Bom.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Bom]:

        return db.scalar(

            select(Bom).where(

                Bom.business_id == business_id, Bom.name == name

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

    ) -> tuple[Sequence[Bom], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Bom.business_id == business_id]

        if not include_cancelled:

            conditions.append(Bom.docstatus != 2)

        if search:

            conditions.append(Bom.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Bom).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Bom)

            .where(*conditions)

            .order_by(Bom.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Bom) -> Bom:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Bom) -> None:

        db.delete(row)

        db.flush()

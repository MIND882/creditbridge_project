"""Data access for BomCreator. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_creator_domain.models.bom_creator import BomCreator

from app.core.pagination import normalise_paging



__all__ = ["BomCreatorRepository"]





class BomCreatorRepository:

    model = BomCreator





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BomCreator]:

        return db.scalar(

            select(BomCreator).where(

                BomCreator.business_id == business_id, BomCreator.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BomCreator]:

        return db.scalar(

            select(BomCreator).where(

                BomCreator.business_id == business_id, BomCreator.name == name

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

    ) -> tuple[Sequence[BomCreator], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BomCreator.business_id == business_id]

        if not include_cancelled:

            conditions.append(BomCreator.docstatus != 2)

        if search:

            conditions.append(BomCreator.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(BomCreator).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BomCreator)

            .where(*conditions)

            .order_by(BomCreator.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: BomCreator) -> BomCreator:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: BomCreator) -> None:

        db.delete(row)

        db.flush()

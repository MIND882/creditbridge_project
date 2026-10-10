"""Data access for IndustryType. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.industry_type_domain.models.industry_type import IndustryType

from app.core.pagination import normalise_paging



__all__ = ["IndustryTypeRepository"]





class IndustryTypeRepository:

    model = IndustryType





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[IndustryType]:

        return db.scalar(

            select(IndustryType).where(

                IndustryType.business_id == business_id, IndustryType.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[IndustryType]:

        return db.scalar(

            select(IndustryType).where(

                IndustryType.business_id == business_id, IndustryType.name == name

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

    ) -> tuple[Sequence[IndustryType], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [IndustryType.business_id == business_id]

        if search:

            conditions.append(IndustryType.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(IndustryType).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(IndustryType)

            .where(*conditions)

            .order_by(IndustryType.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: IndustryType) -> IndustryType:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: IndustryType) -> None:

        db.delete(row)

        db.flush()

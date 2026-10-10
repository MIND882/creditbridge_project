"""Data access for UomCategory. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.uom_category_domain.models.uom_category import UomCategory

from app.core.pagination import normalise_paging



__all__ = ["UomCategoryRepository"]





class UomCategoryRepository:

    model = UomCategory





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[UomCategory]:

        return db.scalar(

            select(UomCategory).where(

                UomCategory.business_id == business_id, UomCategory.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[UomCategory]:

        return db.scalar(

            select(UomCategory).where(

                UomCategory.business_id == business_id, UomCategory.name == name

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

    ) -> tuple[Sequence[UomCategory], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [UomCategory.business_id == business_id]

        if search:

            conditions.append(UomCategory.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(UomCategory).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(UomCategory)

            .where(*conditions)

            .order_by(UomCategory.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: UomCategory) -> UomCategory:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: UomCategory) -> None:

        db.delete(row)

        db.flush()

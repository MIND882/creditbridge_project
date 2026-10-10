"""Data access for Brand. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.brand_domain.models.brand import Brand

from app.core.pagination import normalise_paging



__all__ = ["BrandRepository"]





class BrandRepository:

    model = Brand





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Brand]:

        return db.scalar(

            select(Brand).where(

                Brand.business_id == business_id, Brand.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Brand]:

        return db.scalar(

            select(Brand).where(

                Brand.business_id == business_id, Brand.name == name

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

    ) -> tuple[Sequence[Brand], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Brand.business_id == business_id]

        if search:

            conditions.append(Brand.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Brand).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Brand)

            .where(*conditions)

            .order_by(Brand.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Brand) -> Brand:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Brand) -> None:

        db.delete(row)

        db.flush()

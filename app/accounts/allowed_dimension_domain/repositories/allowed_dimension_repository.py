"""

Data access for Allowed Dimension.



A child table: reads are by parent; writes go through the Accounting Dimension Filter service so

``idx`` ordering stays consistent.

"""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.allowed_dimension_domain.models.allowed_dimension import AllowedDimension

from app.core.pagination import normalise_paging



__all__ = ["AllowedDimensionRepository"]





class AllowedDimensionRepository:

    model = AllowedDimension



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[AllowedDimension]:

        return db.scalar(

            select(AllowedDimension).where(

                AllowedDimension.business_id == business_id, AllowedDimension.id == row_id

            )

        )



    def list_by_parent(

        self, db: Session, business_id: uuid.UUID, parent_id: uuid.UUID

    ) -> list[AllowedDimension]:

        return list(

            db.scalars(

                select(AllowedDimension)

                .where(

                    AllowedDimension.business_id == business_id,

                    AllowedDimension.parent_id == parent_id,

                )

                .order_by(AllowedDimension.idx.asc())

            )

        )



    def list(

        self, db: Session, business_id: uuid.UUID, *, offset: int = 0, limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[AllowedDimension], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [AllowedDimension.business_id == business_id]

        if parent_id is not None:

            conditions.append(AllowedDimension.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(AllowedDimension).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(AllowedDimension).where(*conditions).order_by(AllowedDimension.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: AllowedDimension) -> AllowedDimension:

        db.add(row)

        db.flush()

        return row

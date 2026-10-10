"""Data access for RepostAllowedTypes. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.repost_allowed_types_domain.models.repost_allowed_types import RepostAllowedTypes

from app.core.pagination import normalise_paging



__all__ = ["RepostAllowedTypesRepository"]





class RepostAllowedTypesRepository:

    model = RepostAllowedTypes





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[RepostAllowedTypes]:

        return db.scalar(

            select(RepostAllowedTypes).where(

                RepostAllowedTypes.business_id == business_id, RepostAllowedTypes.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[RepostAllowedTypes], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [RepostAllowedTypes.business_id == business_id]

        if parent_id is not None:

            conditions.append(RepostAllowedTypes.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(RepostAllowedTypes).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(RepostAllowedTypes)

            .where(*conditions)

            .order_by(RepostAllowedTypes.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



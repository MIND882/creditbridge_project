"""Data access for AllowedToTransactWith. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.allowed_to_transact_with_domain.models.allowed_to_transact_with import AllowedToTransactWith

from app.core.pagination import normalise_paging



__all__ = ["AllowedToTransactWithRepository"]





class AllowedToTransactWithRepository:

    model = AllowedToTransactWith





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[AllowedToTransactWith]:

        return db.scalar(

            select(AllowedToTransactWith).where(

                AllowedToTransactWith.business_id == business_id, AllowedToTransactWith.id == row_id

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

    ) -> tuple[Sequence[AllowedToTransactWith], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [AllowedToTransactWith.business_id == business_id]

        if parent_id is not None:

            conditions.append(AllowedToTransactWith.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(AllowedToTransactWith).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(AllowedToTransactWith)

            .where(*conditions)

            .order_by(AllowedToTransactWith.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



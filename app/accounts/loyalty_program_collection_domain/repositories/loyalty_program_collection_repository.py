"""Data access for LoyaltyProgramCollection. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.loyalty_program_collection_domain.models.loyalty_program_collection import LoyaltyProgramCollection

from app.core.pagination import normalise_paging



__all__ = ["LoyaltyProgramCollectionRepository"]





class LoyaltyProgramCollectionRepository:

    model = LoyaltyProgramCollection





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LoyaltyProgramCollection]:

        return db.scalar(

            select(LoyaltyProgramCollection).where(

                LoyaltyProgramCollection.business_id == business_id, LoyaltyProgramCollection.id == row_id

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

    ) -> tuple[Sequence[LoyaltyProgramCollection], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LoyaltyProgramCollection.business_id == business_id]

        if parent_id is not None:

            conditions.append(LoyaltyProgramCollection.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(LoyaltyProgramCollection).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LoyaltyProgramCollection)

            .where(*conditions)

            .order_by(LoyaltyProgramCollection.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



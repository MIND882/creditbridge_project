"""Data access for POSProfileUser. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_profile_user_domain.models.pos_profile_user import POSProfileUser

from app.core.pagination import normalise_paging



__all__ = ["POSProfileUserRepository"]





class POSProfileUserRepository:

    model = POSProfileUser





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSProfileUser]:

        return db.scalar(

            select(POSProfileUser).where(

                POSProfileUser.business_id == business_id, POSProfileUser.id == row_id

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

    ) -> tuple[Sequence[POSProfileUser], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSProfileUser.business_id == business_id]

        if parent_id is not None:

            conditions.append(POSProfileUser.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(POSProfileUser).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSProfileUser)

            .where(*conditions)

            .order_by(POSProfileUser.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



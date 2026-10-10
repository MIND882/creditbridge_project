"""Data access for POSField. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_field_domain.models.pos_field import POSField

from app.core.pagination import normalise_paging



__all__ = ["POSFieldRepository"]





class POSFieldRepository:

    model = POSField





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSField]:

        return db.scalar(

            select(POSField).where(

                POSField.business_id == business_id, POSField.id == row_id

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

    ) -> tuple[Sequence[POSField], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSField.business_id == business_id]

        if parent_id is not None:

            conditions.append(POSField.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(POSField).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSField)

            .where(*conditions)

            .order_by(POSField.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



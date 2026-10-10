"""Data access for SubOperation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.sub_operation_domain.models.sub_operation import SubOperation

from app.core.pagination import normalise_paging



__all__ = ["SubOperationRepository"]





class SubOperationRepository:

    model = SubOperation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SubOperation]:

        return db.scalar(

            select(SubOperation).where(

                SubOperation.business_id == business_id, SubOperation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SubOperation]:

        return db.scalar(

            select(SubOperation).where(

                SubOperation.business_id == business_id, SubOperation.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[SubOperation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SubOperation.business_id == business_id]

        if parent_id is not None:

            conditions.append(SubOperation.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SubOperation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SubOperation)

            .where(*conditions)

            .order_by(SubOperation.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

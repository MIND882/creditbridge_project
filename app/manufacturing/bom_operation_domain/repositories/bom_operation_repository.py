"""Data access for BomOperation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_operation_domain.models.bom_operation import BomOperation

from app.core.pagination import normalise_paging



__all__ = ["BomOperationRepository"]





class BomOperationRepository:

    model = BomOperation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BomOperation]:

        return db.scalar(

            select(BomOperation).where(

                BomOperation.business_id == business_id, BomOperation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BomOperation]:

        return db.scalar(

            select(BomOperation).where(

                BomOperation.business_id == business_id, BomOperation.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BomOperation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BomOperation.business_id == business_id]

        if parent_id is not None:

            conditions.append(BomOperation.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BomOperation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BomOperation)

            .where(*conditions)

            .order_by(BomOperation.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

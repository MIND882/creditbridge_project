"""Data access for Operation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.operation_domain.models.operation import Operation

from app.core.pagination import normalise_paging



__all__ = ["OperationRepository"]





class OperationRepository:

    model = Operation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Operation]:

        return db.scalar(

            select(Operation).where(

                Operation.business_id == business_id, Operation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Operation]:

        return db.scalar(

            select(Operation).where(

                Operation.business_id == business_id, Operation.name == name

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

    ) -> tuple[Sequence[Operation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Operation.business_id == business_id]

        if search:

            conditions.append(Operation.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Operation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Operation)

            .where(*conditions)

            .order_by(Operation.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Operation) -> Operation:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Operation) -> None:

        db.delete(row)

        db.flush()

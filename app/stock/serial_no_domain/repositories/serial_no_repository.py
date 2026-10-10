"""Data access for SerialNo. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.serial_no_domain.models.serial_no import SerialNo

from app.core.pagination import normalise_paging



__all__ = ["SerialNoRepository"]





class SerialNoRepository:

    model = SerialNo





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SerialNo]:

        return db.scalar(

            select(SerialNo).where(

                SerialNo.business_id == business_id, SerialNo.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SerialNo]:

        return db.scalar(

            select(SerialNo).where(

                SerialNo.business_id == business_id, SerialNo.name == name

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

    ) -> tuple[Sequence[SerialNo], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SerialNo.business_id == business_id]

        if search:

            conditions.append(SerialNo.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SerialNo).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SerialNo)

            .where(*conditions)

            .order_by(SerialNo.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SerialNo) -> SerialNo:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SerialNo) -> None:

        db.delete(row)

        db.flush()

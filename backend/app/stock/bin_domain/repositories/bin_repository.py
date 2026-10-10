"""Data access for Bin. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.bin_domain.models.bin import Bin

from app.core.pagination import normalise_paging



__all__ = ["BinRepository"]





class BinRepository:

    model = Bin





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Bin]:

        return db.scalar(

            select(Bin).where(

                Bin.business_id == business_id, Bin.id == row_id

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

    ) -> tuple[Sequence[Bin], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Bin.business_id == business_id]

        if search:

            conditions.append(Bin.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Bin).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Bin)

            .where(*conditions)

            .order_by(Bin.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Bin) -> Bin:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Bin) -> None:

        db.delete(row)

        db.flush()

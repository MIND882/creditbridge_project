"""Data access for PriceList. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.price_list_domain.models.price_list import PriceList

from app.core.pagination import normalise_paging



__all__ = ["PriceListRepository"]





class PriceListRepository:

    model = PriceList





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PriceList]:

        return db.scalar(

            select(PriceList).where(

                PriceList.business_id == business_id, PriceList.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PriceList]:

        return db.scalar(

            select(PriceList).where(

                PriceList.business_id == business_id, PriceList.name == name

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

    ) -> tuple[Sequence[PriceList], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PriceList.business_id == business_id]

        if search:

            conditions.append(PriceList.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PriceList).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PriceList)

            .where(*conditions)

            .order_by(PriceList.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: PriceList) -> PriceList:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PriceList) -> None:

        db.delete(row)

        db.flush()

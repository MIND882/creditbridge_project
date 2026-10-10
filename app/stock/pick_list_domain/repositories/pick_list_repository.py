"""Data access for PickList. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.pick_list_domain.models.pick_list import PickList

from app.core.pagination import normalise_paging



__all__ = ["PickListRepository"]





class PickListRepository:

    model = PickList





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PickList]:

        return db.scalar(

            select(PickList).where(

                PickList.business_id == business_id, PickList.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PickList]:

        return db.scalar(

            select(PickList).where(

                PickList.business_id == business_id, PickList.name == name

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

    ) -> tuple[Sequence[PickList], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PickList.business_id == business_id]

        if not include_cancelled:

            conditions.append(PickList.docstatus != 2)

        if search:

            conditions.append(PickList.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PickList).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PickList)

            .where(*conditions)

            .order_by(PickList.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: PickList) -> PickList:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PickList) -> None:

        db.delete(row)

        db.flush()

"""Data access for BlanketOrder. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.blanket_order_domain.models.blanket_order import BlanketOrder

from app.core.pagination import normalise_paging



__all__ = ["BlanketOrderRepository"]





class BlanketOrderRepository:

    model = BlanketOrder





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BlanketOrder]:

        return db.scalar(

            select(BlanketOrder).where(

                BlanketOrder.business_id == business_id, BlanketOrder.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BlanketOrder]:

        return db.scalar(

            select(BlanketOrder).where(

                BlanketOrder.business_id == business_id, BlanketOrder.name == name

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

    ) -> tuple[Sequence[BlanketOrder], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BlanketOrder.business_id == business_id]

        if not include_cancelled:

            conditions.append(BlanketOrder.docstatus != 2)

        if search:

            conditions.append(BlanketOrder.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(BlanketOrder).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BlanketOrder)

            .where(*conditions)

            .order_by(BlanketOrder.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: BlanketOrder) -> BlanketOrder:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: BlanketOrder) -> None:

        db.delete(row)

        db.flush()

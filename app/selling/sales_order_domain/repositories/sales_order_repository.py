"""Data access for SalesOrder. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.sales_order_domain.models.sales_order import SalesOrder

from app.core.pagination import normalise_paging



__all__ = ["SalesOrderRepository"]





class SalesOrderRepository:

    model = SalesOrder





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesOrder]:

        return db.scalar(

            select(SalesOrder).where(

                SalesOrder.business_id == business_id, SalesOrder.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SalesOrder]:

        return db.scalar(

            select(SalesOrder).where(

                SalesOrder.business_id == business_id, SalesOrder.name == name

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

    ) -> tuple[Sequence[SalesOrder], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesOrder.business_id == business_id]

        if not include_cancelled:

            conditions.append(SalesOrder.docstatus != 2)

        if search:

            conditions.append(SalesOrder.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SalesOrder).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesOrder)

            .where(*conditions)

            .order_by(SalesOrder.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SalesOrder) -> SalesOrder:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SalesOrder) -> None:

        db.delete(row)

        db.flush()

"""Data access for PurchaseOrder. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.purchase_order_domain.models.purchase_order import PurchaseOrder

from app.core.pagination import normalise_paging



__all__ = ["PurchaseOrderRepository"]





class PurchaseOrderRepository:

    model = PurchaseOrder





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PurchaseOrder]:

        return db.scalar(

            select(PurchaseOrder).where(

                PurchaseOrder.business_id == business_id, PurchaseOrder.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PurchaseOrder]:

        return db.scalar(

            select(PurchaseOrder).where(

                PurchaseOrder.business_id == business_id, PurchaseOrder.name == name

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

    ) -> tuple[Sequence[PurchaseOrder], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PurchaseOrder.business_id == business_id]

        if not include_cancelled:

            conditions.append(PurchaseOrder.docstatus != 2)

        if search:

            conditions.append(PurchaseOrder.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PurchaseOrder).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PurchaseOrder)

            .where(*conditions)

            .order_by(PurchaseOrder.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: PurchaseOrder) -> PurchaseOrder:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PurchaseOrder) -> None:

        db.delete(row)

        db.flush()

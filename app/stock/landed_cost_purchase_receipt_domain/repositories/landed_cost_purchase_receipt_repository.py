"""Data access for LandedCostPurchaseReceipt. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.landed_cost_purchase_receipt_domain.models.landed_cost_purchase_receipt import LandedCostPurchaseReceipt

from app.core.pagination import normalise_paging



__all__ = ["LandedCostPurchaseReceiptRepository"]





class LandedCostPurchaseReceiptRepository:

    model = LandedCostPurchaseReceipt





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LandedCostPurchaseReceipt]:

        return db.scalar(

            select(LandedCostPurchaseReceipt).where(

                LandedCostPurchaseReceipt.business_id == business_id, LandedCostPurchaseReceipt.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[LandedCostPurchaseReceipt]:

        return db.scalar(

            select(LandedCostPurchaseReceipt).where(

                LandedCostPurchaseReceipt.business_id == business_id, LandedCostPurchaseReceipt.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[LandedCostPurchaseReceipt], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LandedCostPurchaseReceipt.business_id == business_id]

        if parent_id is not None:

            conditions.append(LandedCostPurchaseReceipt.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(LandedCostPurchaseReceipt).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LandedCostPurchaseReceipt)

            .where(*conditions)

            .order_by(LandedCostPurchaseReceipt.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

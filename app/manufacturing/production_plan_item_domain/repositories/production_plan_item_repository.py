"""Data access for ProductionPlanItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.production_plan_item_domain.models.production_plan_item import ProductionPlanItem

from app.core.pagination import normalise_paging



__all__ = ["ProductionPlanItemRepository"]





class ProductionPlanItemRepository:

    model = ProductionPlanItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProductionPlanItem]:

        return db.scalar(

            select(ProductionPlanItem).where(

                ProductionPlanItem.business_id == business_id, ProductionPlanItem.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ProductionPlanItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProductionPlanItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProductionPlanItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProductionPlanItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProductionPlanItem)

            .where(*conditions)

            .order_by(ProductionPlanItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

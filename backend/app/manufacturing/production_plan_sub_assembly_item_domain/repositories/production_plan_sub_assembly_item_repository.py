"""Data access for ProductionPlanSubAssemblyItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.production_plan_sub_assembly_item_domain.models.production_plan_sub_assembly_item import ProductionPlanSubAssemblyItem

from app.core.pagination import normalise_paging



__all__ = ["ProductionPlanSubAssemblyItemRepository"]





class ProductionPlanSubAssemblyItemRepository:

    model = ProductionPlanSubAssemblyItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProductionPlanSubAssemblyItem]:

        return db.scalar(

            select(ProductionPlanSubAssemblyItem).where(

                ProductionPlanSubAssemblyItem.business_id == business_id, ProductionPlanSubAssemblyItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProductionPlanSubAssemblyItem]:

        return db.scalar(

            select(ProductionPlanSubAssemblyItem).where(

                ProductionPlanSubAssemblyItem.business_id == business_id, ProductionPlanSubAssemblyItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ProductionPlanSubAssemblyItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProductionPlanSubAssemblyItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProductionPlanSubAssemblyItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProductionPlanSubAssemblyItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProductionPlanSubAssemblyItem)

            .where(*conditions)

            .order_by(ProductionPlanSubAssemblyItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

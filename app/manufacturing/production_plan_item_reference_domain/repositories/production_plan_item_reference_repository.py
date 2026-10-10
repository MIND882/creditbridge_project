"""Data access for ProductionPlanItemReference. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.production_plan_item_reference_domain.models.production_plan_item_reference import ProductionPlanItemReference

from app.core.pagination import normalise_paging



__all__ = ["ProductionPlanItemReferenceRepository"]





class ProductionPlanItemReferenceRepository:

    model = ProductionPlanItemReference





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProductionPlanItemReference]:

        return db.scalar(

            select(ProductionPlanItemReference).where(

                ProductionPlanItemReference.business_id == business_id, ProductionPlanItemReference.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProductionPlanItemReference]:

        return db.scalar(

            select(ProductionPlanItemReference).where(

                ProductionPlanItemReference.business_id == business_id, ProductionPlanItemReference.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ProductionPlanItemReference], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProductionPlanItemReference.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProductionPlanItemReference.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProductionPlanItemReference).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProductionPlanItemReference)

            .where(*conditions)

            .order_by(ProductionPlanItemReference.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

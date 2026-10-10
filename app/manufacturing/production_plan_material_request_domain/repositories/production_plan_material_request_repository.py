"""Data access for ProductionPlanMaterialRequest. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.production_plan_material_request_domain.models.production_plan_material_request import ProductionPlanMaterialRequest

from app.core.pagination import normalise_paging



__all__ = ["ProductionPlanMaterialRequestRepository"]





class ProductionPlanMaterialRequestRepository:

    model = ProductionPlanMaterialRequest





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProductionPlanMaterialRequest]:

        return db.scalar(

            select(ProductionPlanMaterialRequest).where(

                ProductionPlanMaterialRequest.business_id == business_id, ProductionPlanMaterialRequest.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ProductionPlanMaterialRequest], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProductionPlanMaterialRequest.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProductionPlanMaterialRequest.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProductionPlanMaterialRequest).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProductionPlanMaterialRequest)

            .where(*conditions)

            .order_by(ProductionPlanMaterialRequest.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

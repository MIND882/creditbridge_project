"""Data access for ProductionPlanMaterialRequestWarehouse. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.production_plan_material_request_warehouse_domain.models.production_plan_material_request_warehouse import ProductionPlanMaterialRequestWarehouse

from app.core.pagination import normalise_paging



__all__ = ["ProductionPlanMaterialRequestWarehouseRepository"]





class ProductionPlanMaterialRequestWarehouseRepository:

    model = ProductionPlanMaterialRequestWarehouse





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProductionPlanMaterialRequestWarehouse]:

        return db.scalar(

            select(ProductionPlanMaterialRequestWarehouse).where(

                ProductionPlanMaterialRequestWarehouse.business_id == business_id, ProductionPlanMaterialRequestWarehouse.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProductionPlanMaterialRequestWarehouse]:

        return db.scalar(

            select(ProductionPlanMaterialRequestWarehouse).where(

                ProductionPlanMaterialRequestWarehouse.business_id == business_id, ProductionPlanMaterialRequestWarehouse.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ProductionPlanMaterialRequestWarehouse], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProductionPlanMaterialRequestWarehouse.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProductionPlanMaterialRequestWarehouse.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProductionPlanMaterialRequestWarehouse).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProductionPlanMaterialRequestWarehouse)

            .where(*conditions)

            .order_by(ProductionPlanMaterialRequestWarehouse.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

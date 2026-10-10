"""Pydantic v2 schemas for ProductionPlanMaterialRequestWarehouse."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProductionPlanMaterialRequestWarehouseCreate",

    "ProductionPlanMaterialRequestWarehouseRead",

    "ProductionPlanMaterialRequestWarehouseListResponse",

]





class ProductionPlanMaterialRequestWarehouseBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    warehouse_id: Optional[uuid.UUID] = None





class ProductionPlanMaterialRequestWarehouseCreate(ProductionPlanMaterialRequestWarehouseBase):

    pass





class ProductionPlanMaterialRequestWarehouseUpdate(InputSchema):

    """A partial update."""



    warehouse_id: Optional[uuid.UUID] = None





class ProductionPlanMaterialRequestWarehouseRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    warehouse_id: Optional[uuid.UUID] = None





ProductionPlanMaterialRequestWarehouseListResponse = Page[ProductionPlanMaterialRequestWarehouseRead]

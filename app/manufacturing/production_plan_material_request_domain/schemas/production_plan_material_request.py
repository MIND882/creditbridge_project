"""Pydantic v2 schemas for ProductionPlanMaterialRequest."""





from __future__ import annotations

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProductionPlanMaterialRequestCreate",

    "ProductionPlanMaterialRequestRead",

    "ProductionPlanMaterialRequestListResponse",

]





class ProductionPlanMaterialRequestBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    material_request_id: uuid.UUID

    material_request_date: Optional[dt.date] = None





class ProductionPlanMaterialRequestCreate(ProductionPlanMaterialRequestBase):

    pass





class ProductionPlanMaterialRequestUpdate(InputSchema):

    """A partial update."""



    material_request_id: Optional[uuid.UUID] = None

    material_request_date: Optional[dt.date] = None





class ProductionPlanMaterialRequestRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    material_request_id: Optional[uuid.UUID] = None

    material_request_date: Optional[dt.date] = None





ProductionPlanMaterialRequestListResponse = Page[ProductionPlanMaterialRequestRead]

"""Pydantic v2 schemas for ProductionPlanItemReference."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProductionPlanItemReferenceCreate",

    "ProductionPlanItemReferenceRead",

    "ProductionPlanItemReferenceListResponse",

]





class ProductionPlanItemReferenceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_reference: Optional[str] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    qty: Optional[Decimal] = None





class ProductionPlanItemReferenceCreate(ProductionPlanItemReferenceBase):

    pass





class ProductionPlanItemReferenceUpdate(InputSchema):

    """A partial update."""



    item_reference: Optional[str] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    qty: Optional[Decimal] = None





class ProductionPlanItemReferenceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_reference: Optional[str] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    qty: Optional[Decimal] = None





ProductionPlanItemReferenceListResponse = Page[ProductionPlanItemReferenceRead]

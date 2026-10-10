"""Pydantic v2 schemas for ItemReorder."""





from __future__ import annotations

from app.stock.item_reorder_domain.models.item_reorder import (

    ItemReorderMaterialRequestType,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemReorderCreate",

    "ItemReorderRead",

    "ItemReorderListResponse",

]





class ItemReorderBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    warehouse_group_id: Optional[uuid.UUID] = None

    warehouse_id: uuid.UUID

    warehouse_reorder_level: Optional[Decimal] = None

    warehouse_reorder_qty: Optional[Decimal] = None

    material_request_type: ItemReorderMaterialRequestType





class ItemReorderCreate(ItemReorderBase):

    pass





class ItemReorderUpdate(InputSchema):

    """A partial update."""



    warehouse_group_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    warehouse_reorder_level: Optional[Decimal] = None

    warehouse_reorder_qty: Optional[Decimal] = None

    material_request_type: Optional[ItemReorderMaterialRequestType] = None





class ItemReorderRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    warehouse_group_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    warehouse_reorder_level: Optional[Decimal] = None

    warehouse_reorder_qty: Optional[Decimal] = None

    material_request_type: Optional[ItemReorderMaterialRequestType] = None





ItemReorderListResponse = Page[ItemReorderRead]

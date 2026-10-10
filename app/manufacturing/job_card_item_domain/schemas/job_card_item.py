"""Pydantic v2 schemas for JobCardItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "JobCardItemCreate",

    "JobCardItemRead",

    "JobCardItemListResponse",

]





class JobCardItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    source_warehouse_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    required_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    consumed_qty: Optional[Decimal] = None

    allow_alternative_item: Optional[bool] = None





class JobCardItemCreate(JobCardItemBase):

    pass





class JobCardItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    required_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    consumed_qty: Optional[Decimal] = None

    allow_alternative_item: Optional[bool] = None





class JobCardItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    required_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    consumed_qty: Optional[Decimal] = None

    allow_alternative_item: Optional[bool] = None





JobCardItemListResponse = Page[JobCardItemRead]

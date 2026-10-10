"""Pydantic v2 schemas for WorkOrderAdditionalItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WorkOrderAdditionalItemCreate",

    "WorkOrderAdditionalItemRead",

    "WorkOrderAdditionalItemListResponse",

]





class WorkOrderAdditionalItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    secondary_item_type: Optional[str] = None

    qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None





class WorkOrderAdditionalItemCreate(WorkOrderAdditionalItemBase):

    pass





class WorkOrderAdditionalItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    secondary_item_type: Optional[str] = None

    qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None





class WorkOrderAdditionalItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    secondary_item_type: Optional[str] = None

    qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None





WorkOrderAdditionalItemListResponse = Page[WorkOrderAdditionalItemRead]

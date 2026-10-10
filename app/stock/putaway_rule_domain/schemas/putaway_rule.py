"""Pydantic v2 schemas for PutawayRule."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PutawayRuleCreate",

    "PutawayRuleUpdate",

    "PutawayRuleRead",

    "PutawayRuleListResponse",

]





class PutawayRuleBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    warehouse_id: uuid.UUID

    capacity: Decimal

    stock_uom_id: Optional[uuid.UUID] = None

    priority: Optional[int] = None

    company: str

    disable: Optional[bool] = None

    uom_id: Optional[uuid.UUID] = None

    stock_capacity: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None





class PutawayRuleCreate(PutawayRuleBase):

    pass





class PutawayRuleUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    capacity: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    priority: Optional[int] = None

    company: Optional[str] = None

    disable: Optional[bool] = None

    uom_id: Optional[uuid.UUID] = None

    stock_capacity: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None





class PutawayRuleRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    capacity: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    priority: Optional[int] = None

    company: str

    disable: Optional[bool] = None

    uom_id: Optional[uuid.UUID] = None

    stock_capacity: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None





PutawayRuleListResponse = Page[PutawayRuleRead]

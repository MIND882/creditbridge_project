"""Pydantic v2 schemas for BlanketOrderItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BlanketOrderItemCreate",

    "BlanketOrderItemRead",

    "BlanketOrderItemListResponse",

]





class BlanketOrderItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    party_item_code: Optional[str] = None

    qty: Optional[Decimal] = None

    rate: Decimal

    ordered_qty: Optional[Decimal] = None

    terms_and_conditions: Optional[str] = None





class BlanketOrderItemCreate(BlanketOrderItemBase):

    pass





class BlanketOrderItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    party_item_code: Optional[str] = None

    qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    terms_and_conditions: Optional[str] = None





class BlanketOrderItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    party_item_code: Optional[str] = None

    qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    terms_and_conditions: Optional[str] = None





BlanketOrderItemListResponse = Page[BlanketOrderItemRead]

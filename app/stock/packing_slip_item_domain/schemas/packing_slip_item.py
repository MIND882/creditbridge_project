"""Pydantic v2 schemas for PackingSlipItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PackingSlipItemCreate",

    "PackingSlipItemRead",

    "PackingSlipItemListResponse",

]





class PackingSlipItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    qty: Decimal

    net_weight: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    weight_uom_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    dn_detail: Optional[str] = None

    pi_detail: Optional[str] = None





class PackingSlipItemCreate(PackingSlipItemBase):

    pass





class PackingSlipItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    qty: Optional[Decimal] = None

    net_weight: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    weight_uom_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    dn_detail: Optional[str] = None

    pi_detail: Optional[str] = None





class PackingSlipItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    qty: Optional[Decimal] = None

    net_weight: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    weight_uom_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    dn_detail: Optional[str] = None

    pi_detail: Optional[str] = None





PackingSlipItemListResponse = Page[PackingSlipItemRead]

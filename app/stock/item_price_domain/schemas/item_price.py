"""Pydantic v2 schemas for ItemPrice."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemPriceCreate",

    "ItemPriceUpdate",

    "ItemPriceRead",

    "ItemPriceListResponse",

]





class ItemPriceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    uom_id: uuid.UUID

    packing_unit: Optional[int] = None

    item_name: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    item_description: Optional[str] = None

    price_list_id: uuid.UUID

    customer: Optional[str] = None

    supplier: Optional[str] = None

    buying: Optional[bool] = None

    selling: Optional[bool] = None

    currency: Optional[str] = None

    price_list_rate: Decimal

    valid_from: Optional[dt.date] = None

    lead_time_days: Optional[int] = None

    valid_upto: Optional[dt.date] = None

    note: Optional[str] = None

    reference: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None





class ItemPriceCreate(ItemPriceBase):

    pass





class ItemPriceUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    packing_unit: Optional[int] = None

    item_name: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    item_description: Optional[str] = None

    price_list_id: Optional[uuid.UUID] = None

    customer: Optional[str] = None

    supplier: Optional[str] = None

    buying: Optional[bool] = None

    selling: Optional[bool] = None

    currency: Optional[str] = None

    price_list_rate: Optional[Decimal] = None

    valid_from: Optional[dt.date] = None

    lead_time_days: Optional[int] = None

    valid_upto: Optional[dt.date] = None

    note: Optional[str] = None

    reference: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None





class ItemPriceRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_code_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    packing_unit: Optional[int] = None

    item_name: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    item_description: Optional[str] = None

    price_list_id: Optional[uuid.UUID] = None

    customer: Optional[str] = None

    supplier: Optional[str] = None

    buying: Optional[bool] = None

    selling: Optional[bool] = None

    currency: Optional[str] = None

    price_list_rate: Optional[Decimal] = None

    valid_from: Optional[dt.date] = None

    lead_time_days: Optional[int] = None

    valid_upto: Optional[dt.date] = None

    note: Optional[str] = None

    reference: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None





ItemPriceListResponse = Page[ItemPriceRead]

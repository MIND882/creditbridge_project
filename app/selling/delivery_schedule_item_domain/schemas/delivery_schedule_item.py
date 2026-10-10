"""Pydantic v2 schemas for DeliveryScheduleItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "DeliveryScheduleItemCreate",

    "DeliveryScheduleItemRead",

    "DeliveryScheduleItemListResponse",

]





class DeliveryScheduleItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    delivery_date: Optional[dt.date] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None





class DeliveryScheduleItemCreate(DeliveryScheduleItemBase):

    pass





class DeliveryScheduleItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    delivery_date: Optional[dt.date] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None





class DeliveryScheduleItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    delivery_date: Optional[dt.date] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None





DeliveryScheduleItemListResponse = Page[DeliveryScheduleItemRead]

"""Pydantic v2 schemas for SalesForecastItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesForecastItemCreate",

    "SalesForecastItemRead",

    "SalesForecastItemListResponse",

]





class SalesForecastItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    uom_id: Optional[uuid.UUID] = None

    delivery_date: Optional[dt.date] = None

    demand_qty: Decimal

    warehouse_id: Optional[uuid.UUID] = None





class SalesForecastItemCreate(SalesForecastItemBase):

    pass





class SalesForecastItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    uom_id: Optional[uuid.UUID] = None

    delivery_date: Optional[dt.date] = None

    demand_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None





class SalesForecastItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    uom_id: Optional[uuid.UUID] = None

    delivery_date: Optional[dt.date] = None

    demand_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None





SalesForecastItemListResponse = Page[SalesForecastItemRead]

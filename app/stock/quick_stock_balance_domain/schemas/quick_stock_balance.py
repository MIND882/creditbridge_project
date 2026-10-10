"""Pydantic v2 schemas for QuickStockBalance."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "QuickStockBalanceUpdate",

    "QuickStockBalanceRead",

]





class QuickStockBalanceUpdate(InputSchema):

    """A partial update of the tenant settings row."""



    warehouse_id: Optional[uuid.UUID] = None

    item_id: Optional[uuid.UUID] = None

    item_barcode: Optional[str] = None

    item_name: Optional[str] = None

    item_description: Optional[str] = None

    qty: Optional[Decimal] = None

    value: Optional[Decimal] = None

    image: Optional[str] = None

    date: Optional[dt.date] = None





class QuickStockBalanceRead(ReadSchema):

    id: uuid.UUID

    warehouse_id: Optional[uuid.UUID] = None

    item_id: Optional[uuid.UUID] = None

    item_barcode: Optional[str] = None

    item_name: Optional[str] = None

    item_description: Optional[str] = None

    qty: Optional[Decimal] = None

    value: Optional[Decimal] = None

    image: Optional[str] = None

    date: Optional[dt.date] = None



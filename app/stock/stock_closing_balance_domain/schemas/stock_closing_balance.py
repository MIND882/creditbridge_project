"""Pydantic v2 schemas for StockClosingBalance."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockClosingBalanceCreate",

    "StockClosingBalanceUpdate",

    "StockClosingBalanceRead",

    "StockClosingBalanceListResponse",

]





class StockClosingBalanceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    posting_datetime: Optional[dt.datetime] = None

    actual_qty: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    stock_value: Optional[Decimal] = None

    company: Optional[str] = None

    stock_uom_id: Optional[uuid.UUID] = None

    stock_value_difference: Optional[Decimal] = None

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    stock_closing_entry_id: Optional[uuid.UUID] = None

    inventory_dimension_key: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    fifo_queue: Optional[str] = None





class StockClosingBalanceCreate(StockClosingBalanceBase):

    pass





class StockClosingBalanceUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    posting_datetime: Optional[dt.datetime] = None

    actual_qty: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    stock_value: Optional[Decimal] = None

    company: Optional[str] = None

    stock_uom_id: Optional[uuid.UUID] = None

    stock_value_difference: Optional[Decimal] = None

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    stock_closing_entry_id: Optional[uuid.UUID] = None

    inventory_dimension_key: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    fifo_queue: Optional[str] = None





class StockClosingBalanceRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_code_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    posting_datetime: Optional[dt.datetime] = None

    actual_qty: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    stock_value: Optional[Decimal] = None

    company: Optional[str] = None

    stock_uom_id: Optional[uuid.UUID] = None

    stock_value_difference: Optional[Decimal] = None

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    stock_closing_entry_id: Optional[uuid.UUID] = None

    inventory_dimension_key: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    fifo_queue: Optional[str] = None





StockClosingBalanceListResponse = Page[StockClosingBalanceRead]

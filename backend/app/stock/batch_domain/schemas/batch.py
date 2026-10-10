"""Pydantic v2 schemas for Batch."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BatchCreate",

    "BatchUpdate",

    "BatchRead",

    "BatchListResponse",

]





class BatchBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    disabled: Optional[bool] = None

    batch_id: str

    item_id: uuid.UUID

    image: Optional[str] = None

    parent_batch_id: Optional[uuid.UUID] = None

    manufacturing_date: Optional[dt.date] = None

    expiry_date: Optional[dt.date] = None

    supplier: Optional[str] = None

    reference_doctype: Optional[str] = None

    reference_name: Optional[str] = None

    description: Optional[str] = None

    item_name: Optional[str] = None

    batch_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    qty_to_produce: Optional[Decimal] = None

    produced_qty: Optional[Decimal] = None

    use_batchwise_valuation: Optional[bool] = None

    allow_negative_stock_for_batch: Optional[bool] = None





class BatchCreate(BatchBase):

    pass





class BatchUpdate(InputSchema):

    """A partial update."""



    disabled: Optional[bool] = None

    batch_id: Optional[str] = None

    item_id: Optional[uuid.UUID] = None

    image: Optional[str] = None

    parent_batch_id: Optional[uuid.UUID] = None

    manufacturing_date: Optional[dt.date] = None

    expiry_date: Optional[dt.date] = None

    supplier: Optional[str] = None

    reference_doctype: Optional[str] = None

    reference_name: Optional[str] = None

    description: Optional[str] = None

    item_name: Optional[str] = None

    batch_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    qty_to_produce: Optional[Decimal] = None

    produced_qty: Optional[Decimal] = None

    use_batchwise_valuation: Optional[bool] = None

    allow_negative_stock_for_batch: Optional[bool] = None





class BatchRead(ReadSchema):

    id: uuid.UUID

    name: str

    disabled: Optional[bool] = None

    batch_id: str

    item_id: Optional[uuid.UUID] = None

    image: Optional[str] = None

    parent_batch_id: Optional[uuid.UUID] = None

    manufacturing_date: Optional[dt.date] = None

    expiry_date: Optional[dt.date] = None

    supplier: Optional[str] = None

    reference_doctype: Optional[str] = None

    reference_name: Optional[str] = None

    description: Optional[str] = None

    item_name: Optional[str] = None

    batch_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    qty_to_produce: Optional[Decimal] = None

    produced_qty: Optional[Decimal] = None

    use_batchwise_valuation: Optional[bool] = None

    allow_negative_stock_for_batch: Optional[bool] = None





BatchListResponse = Page[BatchRead]

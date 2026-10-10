"""Pydantic v2 schemas for SerialAndBatchEntry."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SerialAndBatchEntryCreate",

    "SerialAndBatchEntryRead",

    "SerialAndBatchEntryListResponse",

]





class SerialAndBatchEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    serial_no_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    incoming_rate: Optional[Decimal] = None

    outgoing_rate: Optional[Decimal] = None

    stock_value_difference: Optional[Decimal] = None

    is_outward: Optional[bool] = None

    stock_queue: Optional[str] = None

    delivered_qty: Optional[Decimal] = None

    reference_for_reservation: Optional[str] = None

    posting_datetime: Optional[dt.datetime] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    voucher_detail_no: Optional[str] = None

    type_of_transaction: Optional[str] = None

    is_cancelled: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None





class SerialAndBatchEntryCreate(SerialAndBatchEntryBase):

    pass





class SerialAndBatchEntryUpdate(InputSchema):

    """A partial update."""



    serial_no_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    incoming_rate: Optional[Decimal] = None

    outgoing_rate: Optional[Decimal] = None

    stock_value_difference: Optional[Decimal] = None

    is_outward: Optional[bool] = None

    stock_queue: Optional[str] = None

    delivered_qty: Optional[Decimal] = None

    reference_for_reservation: Optional[str] = None

    posting_datetime: Optional[dt.datetime] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    voucher_detail_no: Optional[str] = None

    type_of_transaction: Optional[str] = None

    is_cancelled: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None





class SerialAndBatchEntryRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    serial_no_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    incoming_rate: Optional[Decimal] = None

    outgoing_rate: Optional[Decimal] = None

    stock_value_difference: Optional[Decimal] = None

    is_outward: Optional[bool] = None

    stock_queue: Optional[str] = None

    delivered_qty: Optional[Decimal] = None

    reference_for_reservation: Optional[str] = None

    posting_datetime: Optional[dt.datetime] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    voucher_detail_no: Optional[str] = None

    type_of_transaction: Optional[str] = None

    is_cancelled: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None





SerialAndBatchEntryListResponse = Page[SerialAndBatchEntryRead]

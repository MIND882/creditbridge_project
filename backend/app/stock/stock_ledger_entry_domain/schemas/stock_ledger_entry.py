"""Pydantic v2 schemas for StockLedgerEntry."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockLedgerEntryCreate",

    "StockLedgerEntryUpdate",

    "StockLedgerEntryRead",

    "StockLedgerEntryListResponse",

]





class StockLedgerEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    batch_no: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    voucher_detail_no: Optional[str] = None

    actual_qty: Optional[Decimal] = None

    incoming_rate: Optional[Decimal] = None

    outgoing_rate: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    qty_after_transaction: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    stock_value: Optional[Decimal] = None

    stock_value_difference: Optional[Decimal] = None

    stock_queue: Optional[str] = None

    project: Optional[str] = None

    company: Optional[str] = None

    fiscal_year: Optional[str] = None

    is_cancelled: Optional[bool] = None

    to_rename: Optional[bool] = None

    dependant_sle_voucher_detail_no: Optional[str] = None

    recalculate_rate: Optional[bool] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    has_batch_no: Optional[bool] = None

    has_serial_no: Optional[bool] = None

    is_adjustment_entry: Optional[bool] = None

    auto_created_serial_and_batch_bundle: Optional[bool] = None

    posting_datetime: Optional[dt.datetime] = None





class StockLedgerEntryCreate(StockLedgerEntryBase):

    pass





class StockLedgerEntryUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    batch_no: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    voucher_detail_no: Optional[str] = None

    actual_qty: Optional[Decimal] = None

    incoming_rate: Optional[Decimal] = None

    outgoing_rate: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    qty_after_transaction: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    stock_value: Optional[Decimal] = None

    stock_value_difference: Optional[Decimal] = None

    stock_queue: Optional[str] = None

    project: Optional[str] = None

    company: Optional[str] = None

    fiscal_year: Optional[str] = None

    is_cancelled: Optional[bool] = None

    to_rename: Optional[bool] = None

    dependant_sle_voucher_detail_no: Optional[str] = None

    recalculate_rate: Optional[bool] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    has_batch_no: Optional[bool] = None

    has_serial_no: Optional[bool] = None

    is_adjustment_entry: Optional[bool] = None

    auto_created_serial_and_batch_bundle: Optional[bool] = None

    posting_datetime: Optional[dt.datetime] = None





class StockLedgerEntryRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_code_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    batch_no: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    voucher_detail_no: Optional[str] = None

    actual_qty: Optional[Decimal] = None

    incoming_rate: Optional[Decimal] = None

    outgoing_rate: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    qty_after_transaction: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    stock_value: Optional[Decimal] = None

    stock_value_difference: Optional[Decimal] = None

    stock_queue: Optional[str] = None

    project: Optional[str] = None

    company: Optional[str] = None

    fiscal_year: Optional[str] = None

    is_cancelled: Optional[bool] = None

    to_rename: Optional[bool] = None

    dependant_sle_voucher_detail_no: Optional[str] = None

    recalculate_rate: Optional[bool] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    has_batch_no: Optional[bool] = None

    has_serial_no: Optional[bool] = None

    is_adjustment_entry: Optional[bool] = None

    auto_created_serial_and_batch_bundle: Optional[bool] = None

    posting_datetime: Optional[dt.datetime] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





StockLedgerEntryListResponse = Page[StockLedgerEntryRead]

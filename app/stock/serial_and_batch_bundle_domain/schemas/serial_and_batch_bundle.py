"""Pydantic v2 schemas for SerialAndBatchBundle."""





from __future__ import annotations

from app.stock.serial_and_batch_bundle_domain.models.serial_and_batch_bundle import (

    SerialAndBatchBundleTypeOfTransaction,

    SerialAndBatchBundleNamingSeries,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.serial_and_batch_entry_domain.schemas.serial_and_batch_entry import (

    SerialAndBatchEntryCreate,

    SerialAndBatchEntryRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SerialAndBatchBundleCreate",

    "SerialAndBatchBundleUpdate",

    "SerialAndBatchBundleRead",

    "SerialAndBatchBundleListResponse",

]





class SerialAndBatchBundleBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    company: str

    item_group_id: Optional[uuid.UUID] = None

    has_serial_no: Optional[bool] = None

    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    has_batch_no: Optional[bool] = None

    voucher_type: str

    voucher_no: Optional[str] = None

    is_cancelled: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    avg_rate: Optional[Decimal] = None

    total_amount: Optional[Decimal] = None

    total_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    type_of_transaction: SerialAndBatchBundleTypeOfTransaction

    is_rejected: Optional[bool] = None

    voucher_detail_no: Optional[str] = None

    returned_against: Optional[str] = None

    naming_series: Optional[SerialAndBatchBundleNamingSeries] = None

    is_packed: Optional[bool] = None

    posting_datetime: Optional[dt.datetime] = None

    entries: list[SerialAndBatchEntryCreate] = []





class SerialAndBatchBundleCreate(SerialAndBatchBundleBase):

    pass





class SerialAndBatchBundleUpdate(InputSchema):

    """A partial update."""



    company: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    has_serial_no: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    has_batch_no: Optional[bool] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    is_cancelled: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    avg_rate: Optional[Decimal] = None

    total_amount: Optional[Decimal] = None

    total_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    type_of_transaction: Optional[SerialAndBatchBundleTypeOfTransaction] = None

    is_rejected: Optional[bool] = None

    voucher_detail_no: Optional[str] = None

    returned_against: Optional[str] = None

    naming_series: Optional[SerialAndBatchBundleNamingSeries] = None

    is_packed: Optional[bool] = None

    posting_datetime: Optional[dt.datetime] = None

    entries: Optional[list[SerialAndBatchEntryCreate]] = None





class SerialAndBatchBundleRead(ReadSchema):

    id: uuid.UUID

    name: str

    company: str

    item_group_id: Optional[uuid.UUID] = None

    has_serial_no: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    has_batch_no: Optional[bool] = None

    voucher_type: str

    voucher_no: Optional[str] = None

    is_cancelled: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    avg_rate: Optional[Decimal] = None

    total_amount: Optional[Decimal] = None

    total_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    type_of_transaction: Optional[SerialAndBatchBundleTypeOfTransaction] = None

    is_rejected: Optional[bool] = None

    voucher_detail_no: Optional[str] = None

    returned_against: Optional[str] = None

    naming_series: Optional[SerialAndBatchBundleNamingSeries] = None

    is_packed: Optional[bool] = None

    posting_datetime: Optional[dt.datetime] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    entries: list[SerialAndBatchEntryRead] = []





SerialAndBatchBundleListResponse = Page[SerialAndBatchBundleRead]

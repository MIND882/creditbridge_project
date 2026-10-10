"""Pydantic v2 schemas for StockReservationEntry."""





from __future__ import annotations

from app.stock.stock_reservation_entry_domain.models.stock_reservation_entry import (

    StockReservationEntryVoucherType,

    StockReservationEntryStatus,

    StockReservationEntryReservationBasedOn,

    StockReservationEntryFromVoucherType,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockReservationEntryCreate",

    "StockReservationEntryUpdate",

    "StockReservationEntryRead",

    "StockReservationEntryListResponse",

]





class StockReservationEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    voucher_type: Optional[StockReservationEntryVoucherType] = None

    voucher_no: Optional[str] = None

    voucher_detail_no: Optional[str] = None

    stock_uom_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    company: Optional[str] = None

    reserved_qty: Optional[Decimal] = None

    status: Optional[StockReservationEntryStatus] = None

    delivered_qty: Optional[Decimal] = None

    amended_from_id: Optional[uuid.UUID] = None

    available_qty: Optional[Decimal] = None

    voucher_qty: Optional[Decimal] = None

    has_serial_no: Optional[bool] = None

    has_batch_no: Optional[bool] = None

    reservation_based_on: Optional[StockReservationEntryReservationBasedOn] = None

    from_voucher_type: Optional[StockReservationEntryFromVoucherType] = None

    from_voucher_detail_no: Optional[str] = None

    from_voucher_no: Optional[str] = None

    consumed_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None





class StockReservationEntryCreate(StockReservationEntryBase):

    pass





class StockReservationEntryUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    voucher_type: Optional[StockReservationEntryVoucherType] = None

    voucher_no: Optional[str] = None

    voucher_detail_no: Optional[str] = None

    stock_uom_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    company: Optional[str] = None

    reserved_qty: Optional[Decimal] = None

    status: Optional[StockReservationEntryStatus] = None

    delivered_qty: Optional[Decimal] = None

    amended_from_id: Optional[uuid.UUID] = None

    available_qty: Optional[Decimal] = None

    voucher_qty: Optional[Decimal] = None

    has_serial_no: Optional[bool] = None

    has_batch_no: Optional[bool] = None

    reservation_based_on: Optional[StockReservationEntryReservationBasedOn] = None

    from_voucher_type: Optional[StockReservationEntryFromVoucherType] = None

    from_voucher_detail_no: Optional[str] = None

    from_voucher_no: Optional[str] = None

    consumed_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None





class StockReservationEntryRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_code_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    voucher_type: Optional[StockReservationEntryVoucherType] = None

    voucher_no: Optional[str] = None

    voucher_detail_no: Optional[str] = None

    stock_uom_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    company: Optional[str] = None

    reserved_qty: Optional[Decimal] = None

    status: Optional[StockReservationEntryStatus] = None

    delivered_qty: Optional[Decimal] = None

    amended_from_id: Optional[uuid.UUID] = None

    available_qty: Optional[Decimal] = None

    voucher_qty: Optional[Decimal] = None

    has_serial_no: Optional[bool] = None

    has_batch_no: Optional[bool] = None

    reservation_based_on: Optional[StockReservationEntryReservationBasedOn] = None

    from_voucher_type: Optional[StockReservationEntryFromVoucherType] = None

    from_voucher_detail_no: Optional[str] = None

    from_voucher_no: Optional[str] = None

    consumed_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





StockReservationEntryListResponse = Page[StockReservationEntryRead]

"""Pydantic v2 schemas for RepostItemValuation."""





from __future__ import annotations

from app.stock.repost_item_valuation_domain.models.repost_item_valuation import (

    RepostItemValuationStatus,

    RepostItemValuationBasedOn,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "RepostItemValuationCreate",

    "RepostItemValuationUpdate",

    "RepostItemValuationRead",

    "RepostItemValuationListResponse",

]





class RepostItemValuationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    posting_date: dt.date

    posting_time: Optional[dt.time] = None

    status: Optional[RepostItemValuationStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    error_log: Optional[str] = None

    company: Optional[str] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    based_on: RepostItemValuationBasedOn

    allow_negative_stock: Optional[bool] = None

    via_landed_cost_voucher: Optional[bool] = None

    allow_zero_rate: Optional[bool] = None

    items_to_be_repost: Optional[str] = None

    current_index: Optional[int] = None

    gl_reposting_index: Optional[int] = None

    total_reposting_count: Optional[int] = None

    recreate_stock_ledgers: Optional[bool] = None

    reposting_reference: Optional[str] = None

    repost_only_accounting_ledgers: Optional[bool] = None

    total_vouchers: Optional[int] = None

    vouchers_posted: Optional[int] = None

    reposting_data_file: Optional[str] = None

    recalculate_valuation_rate: Optional[bool] = None





class RepostItemValuationCreate(RepostItemValuationBase):

    pass





class RepostItemValuationUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    status: Optional[RepostItemValuationStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    error_log: Optional[str] = None

    company: Optional[str] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    based_on: Optional[RepostItemValuationBasedOn] = None

    allow_negative_stock: Optional[bool] = None

    via_landed_cost_voucher: Optional[bool] = None

    allow_zero_rate: Optional[bool] = None

    items_to_be_repost: Optional[str] = None

    current_index: Optional[int] = None

    gl_reposting_index: Optional[int] = None

    total_reposting_count: Optional[int] = None

    recreate_stock_ledgers: Optional[bool] = None

    reposting_reference: Optional[str] = None

    repost_only_accounting_ledgers: Optional[bool] = None

    total_vouchers: Optional[int] = None

    vouchers_posted: Optional[int] = None

    reposting_data_file: Optional[str] = None

    recalculate_valuation_rate: Optional[bool] = None





class RepostItemValuationRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_code_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    status: Optional[RepostItemValuationStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    error_log: Optional[str] = None

    company: Optional[str] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    based_on: Optional[RepostItemValuationBasedOn] = None

    allow_negative_stock: Optional[bool] = None

    via_landed_cost_voucher: Optional[bool] = None

    allow_zero_rate: Optional[bool] = None

    items_to_be_repost: Optional[str] = None

    current_index: Optional[int] = None

    gl_reposting_index: Optional[int] = None

    total_reposting_count: Optional[int] = None

    recreate_stock_ledgers: Optional[bool] = None

    reposting_reference: Optional[str] = None

    repost_only_accounting_ledgers: Optional[bool] = None

    total_vouchers: Optional[int] = None

    vouchers_posted: Optional[int] = None

    reposting_data_file: Optional[str] = None

    recalculate_valuation_rate: Optional[bool] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





RepostItemValuationListResponse = Page[RepostItemValuationRead]

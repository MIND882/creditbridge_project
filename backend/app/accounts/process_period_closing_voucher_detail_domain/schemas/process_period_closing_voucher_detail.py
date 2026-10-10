"""Pydantic v2 schemas for ProcessPeriodClosingVoucherDetail."""





from __future__ import annotations

from app.accounts.process_period_closing_voucher_detail_domain.models.process_period_closing_voucher_detail import (

    ProcessPeriodClosingVoucherDetailReportType,

    ProcessPeriodClosingVoucherDetailStatus,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProcessPeriodClosingVoucherDetailCreate",

    "ProcessPeriodClosingVoucherDetailRead",

    "ProcessPeriodClosingVoucherDetailListResponse",

]





class ProcessPeriodClosingVoucherDetailBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    processing_date: Optional[dt.date] = None

    status: Optional[ProcessPeriodClosingVoucherDetailStatus] = None

    closing_balance: Optional[str] = None

    report_type: Optional[ProcessPeriodClosingVoucherDetailReportType] = None





class ProcessPeriodClosingVoucherDetailCreate(ProcessPeriodClosingVoucherDetailBase):

    """Accepted only nested inside the parent payload."""

    pass





class ProcessPeriodClosingVoucherDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    processing_date: Optional[dt.date] = None

    status: Optional[ProcessPeriodClosingVoucherDetailStatus] = None

    closing_balance: Optional[str] = None

    report_type: Optional[ProcessPeriodClosingVoucherDetailReportType] = None





ProcessPeriodClosingVoucherDetailListResponse = Page[ProcessPeriodClosingVoucherDetailRead]

"""Pydantic v2 schemas for PeriodClosingVoucher."""





from __future__ import annotations

from app.accounts.period_closing_voucher_domain.models.period_closing_voucher import (

    PeriodClosingVoucherGleProcessingStatus,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PeriodClosingVoucherCreate",

    "PeriodClosingVoucherUpdate",

    "PeriodClosingVoucherRead",

    "PeriodClosingVoucherListResponse",

]





class PeriodClosingVoucherBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    transaction_date: Optional[dt.date] = None

    fiscal_year_id: uuid.UUID

    amended_from: Optional[str] = None

    closing_account_head_id: uuid.UUID

    remarks: str

    gle_processing_status: Optional[PeriodClosingVoucherGleProcessingStatus] = None

    error_message: Optional[str] = None

    period_end_date: dt.date

    period_start_date: dt.date





class PeriodClosingVoucherCreate(PeriodClosingVoucherBase):

    pass





class PeriodClosingVoucherUpdate(InputSchema):

    """A partial update."""



    transaction_date: Optional[dt.date] = None

    fiscal_year_id: Optional[uuid.UUID] = None

    amended_from: Optional[str] = None

    closing_account_head_id: Optional[uuid.UUID] = None

    remarks: Optional[str] = None

    gle_processing_status: Optional[PeriodClosingVoucherGleProcessingStatus] = None

    error_message: Optional[str] = None

    period_end_date: Optional[dt.date] = None

    period_start_date: Optional[dt.date] = None





class PeriodClosingVoucherRead(ReadSchema):

    id: uuid.UUID

    name: str

    transaction_date: Optional[dt.date] = None

    fiscal_year_id: uuid.UUID

    amended_from: Optional[str] = None

    closing_account_head_id: uuid.UUID

    remarks: str

    gle_processing_status: Optional[PeriodClosingVoucherGleProcessingStatus] = None

    error_message: Optional[str] = None

    period_end_date: dt.date

    period_start_date: dt.date



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





PeriodClosingVoucherListResponse = Page[PeriodClosingVoucherRead]

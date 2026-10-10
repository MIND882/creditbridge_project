"""Pydantic v2 schemas for SalesInvoiceTimesheet."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesInvoiceTimesheetCreate",

    "SalesInvoiceTimesheetRead",

    "SalesInvoiceTimesheetListResponse",

]





class SalesInvoiceTimesheetBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    time_sheet: Optional[str] = None

    billing_hours: Optional[Decimal] = None

    billing_amount: Optional[Decimal] = None

    timesheet_detail: Optional[str] = None

    activity_type: Optional[str] = None

    description: Optional[str] = None

    from_time: Optional[dt.datetime] = None

    to_time: Optional[dt.datetime] = None

    project_name: Optional[str] = None





class SalesInvoiceTimesheetCreate(SalesInvoiceTimesheetBase):

    """Accepted only nested inside the parent payload."""

    pass





class SalesInvoiceTimesheetRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    time_sheet: Optional[str] = None

    billing_hours: Optional[Decimal] = None

    billing_amount: Optional[Decimal] = None

    timesheet_detail: Optional[str] = None

    activity_type: Optional[str] = None

    description: Optional[str] = None

    from_time: Optional[dt.datetime] = None

    to_time: Optional[dt.datetime] = None

    project_name: Optional[str] = None





SalesInvoiceTimesheetListResponse = Page[SalesInvoiceTimesheetRead]

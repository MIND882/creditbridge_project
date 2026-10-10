"""Pydantic v2 schemas for DowntimeEntry."""





from __future__ import annotations

from app.manufacturing.downtime_entry_domain.models.downtime_entry import (

    DowntimeEntryNamingSeries,

    DowntimeEntryStopReason,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "DowntimeEntryCreate",

    "DowntimeEntryUpdate",

    "DowntimeEntryRead",

    "DowntimeEntryListResponse",

]





class DowntimeEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: DowntimeEntryNamingSeries

    workstation_id: uuid.UUID

    operator: str

    from_time: dt.datetime

    to_time: dt.datetime

    downtime: Optional[Decimal] = None

    stop_reason: DowntimeEntryStopReason

    remarks: Optional[str] = None





class DowntimeEntryCreate(DowntimeEntryBase):

    pass





class DowntimeEntryUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[DowntimeEntryNamingSeries] = None

    workstation_id: Optional[uuid.UUID] = None

    operator: Optional[str] = None

    from_time: Optional[dt.datetime] = None

    to_time: Optional[dt.datetime] = None

    downtime: Optional[Decimal] = None

    stop_reason: Optional[DowntimeEntryStopReason] = None

    remarks: Optional[str] = None





class DowntimeEntryRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[DowntimeEntryNamingSeries] = None

    workstation_id: Optional[uuid.UUID] = None

    operator: str

    from_time: Optional[dt.datetime] = None

    to_time: Optional[dt.datetime] = None

    downtime: Optional[Decimal] = None

    stop_reason: Optional[DowntimeEntryStopReason] = None

    remarks: Optional[str] = None





DowntimeEntryListResponse = Page[DowntimeEntryRead]

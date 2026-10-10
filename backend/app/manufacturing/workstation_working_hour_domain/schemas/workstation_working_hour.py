"""Pydantic v2 schemas for WorkstationWorkingHour."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WorkstationWorkingHourCreate",

    "WorkstationWorkingHourRead",

    "WorkstationWorkingHourListResponse",

]





class WorkstationWorkingHourBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    start_time: dt.time

    hours: Optional[Decimal] = None

    end_time: dt.time

    enabled: Optional[bool] = None





class WorkstationWorkingHourCreate(WorkstationWorkingHourBase):

    pass





class WorkstationWorkingHourUpdate(InputSchema):

    """A partial update."""



    start_time: Optional[dt.time] = None

    hours: Optional[Decimal] = None

    end_time: Optional[dt.time] = None

    enabled: Optional[bool] = None





class WorkstationWorkingHourRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    start_time: Optional[dt.time] = None

    hours: Optional[Decimal] = None

    end_time: Optional[dt.time] = None

    enabled: Optional[bool] = None





WorkstationWorkingHourListResponse = Page[WorkstationWorkingHourRead]

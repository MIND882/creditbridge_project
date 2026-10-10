"""Pydantic v2 schemas for JobCardTimeLog."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "JobCardTimeLogCreate",

    "JobCardTimeLogRead",

    "JobCardTimeLogListResponse",

]





class JobCardTimeLogBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    employee: Optional[str] = None

    from_time: Optional[dt.datetime] = None

    to_time: Optional[dt.datetime] = None

    time_in_mins: Optional[Decimal] = None

    completed_qty: Optional[Decimal] = None

    operation_id: Optional[uuid.UUID] = None





class JobCardTimeLogCreate(JobCardTimeLogBase):

    pass





class JobCardTimeLogUpdate(InputSchema):

    """A partial update."""



    employee: Optional[str] = None

    from_time: Optional[dt.datetime] = None

    to_time: Optional[dt.datetime] = None

    time_in_mins: Optional[Decimal] = None

    completed_qty: Optional[Decimal] = None

    operation_id: Optional[uuid.UUID] = None





class JobCardTimeLogRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    employee: Optional[str] = None

    from_time: Optional[dt.datetime] = None

    to_time: Optional[dt.datetime] = None

    time_in_mins: Optional[Decimal] = None

    completed_qty: Optional[Decimal] = None

    operation_id: Optional[uuid.UUID] = None





JobCardTimeLogListResponse = Page[JobCardTimeLogRead]

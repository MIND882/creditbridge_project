"""Pydantic v2 schemas for JobCardScheduledTime."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "JobCardScheduledTimeCreate",

    "JobCardScheduledTimeRead",

    "JobCardScheduledTimeListResponse",

]





class JobCardScheduledTimeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    from_time: Optional[dt.datetime] = None

    to_time: Optional[dt.datetime] = None

    time_in_mins: Optional[Decimal] = None





class JobCardScheduledTimeCreate(JobCardScheduledTimeBase):

    pass





class JobCardScheduledTimeUpdate(InputSchema):

    """A partial update."""



    from_time: Optional[dt.datetime] = None

    to_time: Optional[dt.datetime] = None

    time_in_mins: Optional[Decimal] = None





class JobCardScheduledTimeRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    from_time: Optional[dt.datetime] = None

    to_time: Optional[dt.datetime] = None

    time_in_mins: Optional[Decimal] = None





JobCardScheduledTimeListResponse = Page[JobCardScheduledTimeRead]

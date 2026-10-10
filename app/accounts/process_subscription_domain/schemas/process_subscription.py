"""Pydantic v2 schemas for ProcessSubscription."""





from __future__ import annotations

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProcessSubscriptionCreate",

    "ProcessSubscriptionUpdate",

    "ProcessSubscriptionRead",

    "ProcessSubscriptionListResponse",

]





class ProcessSubscriptionBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    amended_from: Optional[str] = None

    posting_date: dt.date

    subscription: Optional[str] = None





class ProcessSubscriptionCreate(ProcessSubscriptionBase):

    pass





class ProcessSubscriptionUpdate(InputSchema):

    """A partial update."""



    amended_from: Optional[str] = None

    posting_date: Optional[dt.date] = None

    subscription: Optional[str] = None





class ProcessSubscriptionRead(ReadSchema):

    id: uuid.UUID

    name: str

    amended_from: Optional[str] = None

    posting_date: dt.date

    subscription: Optional[str] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





ProcessSubscriptionListResponse = Page[ProcessSubscriptionRead]

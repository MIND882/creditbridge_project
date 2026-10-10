"""Pydantic v2 schemas for POSOpeningEntry."""





from __future__ import annotations

from app.accounts.pos_opening_entry_domain.models.pos_opening_entry import (

    POSOpeningEntryStatus,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.pos_opening_entry_detail_domain.schemas.pos_opening_entry_detail import (

    POSOpeningEntryDetailCreate,

    POSOpeningEntryDetailRead,

)



__all__ = [

    "POSOpeningEntryCreate",

    "POSOpeningEntryUpdate",

    "POSOpeningEntryRead",

    "POSOpeningEntryListResponse",

]





class POSOpeningEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    period_start_date: Optional[dt.datetime] = None

    period_end_date: Optional[dt.date] = None

    posting_date: dt.date

    pos_profile: str

    user: str

    amended_from: Optional[str] = None

    set_posting_date: Optional[bool] = None

    status: Optional[POSOpeningEntryStatus] = None

    pos_closing_entry: Optional[str] = None



    balance_details: list[POSOpeningEntryDetailCreate] = []





class POSOpeningEntryCreate(POSOpeningEntryBase):

    pass





class POSOpeningEntryUpdate(InputSchema):

    """A partial update."""



    period_start_date: Optional[dt.datetime] = None

    period_end_date: Optional[dt.date] = None

    posting_date: Optional[dt.date] = None

    pos_profile: Optional[str] = None

    user: Optional[str] = None

    amended_from: Optional[str] = None

    set_posting_date: Optional[bool] = None

    status: Optional[POSOpeningEntryStatus] = None

    pos_closing_entry: Optional[str] = None

    balance_details: Optional[list[POSOpeningEntryDetailCreate]] = None





class POSOpeningEntryRead(ReadSchema):

    id: uuid.UUID

    name: str

    period_start_date: Optional[dt.datetime] = None

    period_end_date: Optional[dt.date] = None

    posting_date: dt.date

    pos_profile: str

    user: str

    amended_from: Optional[str] = None

    set_posting_date: bool

    status: Optional[POSOpeningEntryStatus] = None

    pos_closing_entry: Optional[str] = None

    balance_details: list[POSOpeningEntryDetailRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





POSOpeningEntryListResponse = Page[POSOpeningEntryRead]

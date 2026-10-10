"""Pydantic v2 schemas for StockClosingEntry."""





from __future__ import annotations

from app.stock.stock_closing_entry_domain.models.stock_closing_entry import (

    StockClosingEntryNamingSeries,

    StockClosingEntryStatus,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockClosingEntryCreate",

    "StockClosingEntryUpdate",

    "StockClosingEntryRead",

    "StockClosingEntryListResponse",

]





class StockClosingEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: Optional[StockClosingEntryNamingSeries] = None

    company: Optional[str] = None

    status: Optional[StockClosingEntryStatus] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    amended_from_id: Optional[uuid.UUID] = None





class StockClosingEntryCreate(StockClosingEntryBase):

    pass





class StockClosingEntryUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[StockClosingEntryNamingSeries] = None

    company: Optional[str] = None

    status: Optional[StockClosingEntryStatus] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    amended_from_id: Optional[uuid.UUID] = None





class StockClosingEntryRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[StockClosingEntryNamingSeries] = None

    company: Optional[str] = None

    status: Optional[StockClosingEntryStatus] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    amended_from_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





StockClosingEntryListResponse = Page[StockClosingEntryRead]

"""Pydantic v2 schemas for ProcessDeferredAccounting."""





from __future__ import annotations

from app.accounts.process_deferred_accounting_domain.models.process_deferred_accounting import (

    ProcessDeferredAccountingType,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProcessDeferredAccountingCreate",

    "ProcessDeferredAccountingUpdate",

    "ProcessDeferredAccountingRead",

    "ProcessDeferredAccountingListResponse",

]





class ProcessDeferredAccountingBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    type: ProcessDeferredAccountingType

    amended_from: Optional[str] = None

    start_date: dt.date

    end_date: dt.date

    posting_date: dt.date

    account_id: Optional[uuid.UUID] = None





class ProcessDeferredAccountingCreate(ProcessDeferredAccountingBase):

    pass





class ProcessDeferredAccountingUpdate(InputSchema):

    """A partial update."""



    type: Optional[ProcessDeferredAccountingType] = None

    amended_from: Optional[str] = None

    start_date: Optional[dt.date] = None

    end_date: Optional[dt.date] = None

    posting_date: Optional[dt.date] = None

    account_id: Optional[uuid.UUID] = None





class ProcessDeferredAccountingRead(ReadSchema):

    id: uuid.UUID

    name: str

    type: ProcessDeferredAccountingType

    amended_from: Optional[str] = None

    start_date: dt.date

    end_date: dt.date

    posting_date: dt.date

    account_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





ProcessDeferredAccountingListResponse = Page[ProcessDeferredAccountingRead]

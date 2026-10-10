"""Pydantic v2 schemas for RepostAccountingLedger."""





from __future__ import annotations

from app.accounts.repost_accounting_ledger_domain.models.repost_accounting_ledger import (

    RepostAccountingLedgerStatus,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.repost_accounting_ledger_items_domain.schemas.repost_accounting_ledger_items import (

    RepostAccountingLedgerItemsCreate,

    RepostAccountingLedgerItemsRead,

)



__all__ = [

    "RepostAccountingLedgerCreate",

    "RepostAccountingLedgerUpdate",

    "RepostAccountingLedgerRead",

    "RepostAccountingLedgerListResponse",

]





class RepostAccountingLedgerBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    amended_from: Optional[str] = None

    delete_cancelled_entries: Optional[bool] = None

    error_log: Optional[str] = None

    status: Optional[RepostAccountingLedgerStatus] = None

    scheduled_job: Optional[str] = None



    vouchers: list[RepostAccountingLedgerItemsCreate] = []





class RepostAccountingLedgerCreate(RepostAccountingLedgerBase):

    pass





class RepostAccountingLedgerUpdate(InputSchema):

    """A partial update."""



    amended_from: Optional[str] = None

    delete_cancelled_entries: Optional[bool] = None

    error_log: Optional[str] = None

    status: Optional[RepostAccountingLedgerStatus] = None

    scheduled_job: Optional[str] = None

    vouchers: Optional[list[RepostAccountingLedgerItemsCreate]] = None





class RepostAccountingLedgerRead(ReadSchema):

    id: uuid.UUID

    name: str

    amended_from: Optional[str] = None

    delete_cancelled_entries: bool

    error_log: Optional[str] = None

    status: Optional[RepostAccountingLedgerStatus] = None

    scheduled_job: Optional[str] = None

    vouchers: list[RepostAccountingLedgerItemsRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





RepostAccountingLedgerListResponse = Page[RepostAccountingLedgerRead]

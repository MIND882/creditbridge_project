"""Pydantic v2 schemas for RepostPaymentLedger."""





from __future__ import annotations

from app.accounts.repost_payment_ledger_domain.models.repost_payment_ledger import (

    RepostPaymentLedgerRepostStatus,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.repost_payment_ledger_items_domain.schemas.repost_payment_ledger_items import (

    RepostPaymentLedgerItemsCreate,

    RepostPaymentLedgerItemsRead,

)



__all__ = [

    "RepostPaymentLedgerCreate",

    "RepostPaymentLedgerUpdate",

    "RepostPaymentLedgerRead",

    "RepostPaymentLedgerListResponse",

]





class RepostPaymentLedgerBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    posting_date: dt.date

    voucher_type: Optional[str] = None

    amended_from: Optional[str] = None

    repost_status: Optional[RepostPaymentLedgerRepostStatus] = None

    add_manually: Optional[bool] = None

    repost_error_log: Optional[str] = None



    repost_vouchers: list[RepostPaymentLedgerItemsCreate] = []





class RepostPaymentLedgerCreate(RepostPaymentLedgerBase):

    pass





class RepostPaymentLedgerUpdate(InputSchema):

    """A partial update."""



    posting_date: Optional[dt.date] = None

    voucher_type: Optional[str] = None

    amended_from: Optional[str] = None

    repost_status: Optional[RepostPaymentLedgerRepostStatus] = None

    add_manually: Optional[bool] = None

    repost_error_log: Optional[str] = None

    repost_vouchers: Optional[list[RepostPaymentLedgerItemsCreate]] = None





class RepostPaymentLedgerRead(ReadSchema):

    id: uuid.UUID

    name: str

    posting_date: dt.date

    voucher_type: Optional[str] = None

    amended_from: Optional[str] = None

    repost_status: Optional[RepostPaymentLedgerRepostStatus] = None

    add_manually: bool

    repost_error_log: Optional[str] = None

    repost_vouchers: list[RepostPaymentLedgerItemsRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





RepostPaymentLedgerListResponse = Page[RepostPaymentLedgerRead]

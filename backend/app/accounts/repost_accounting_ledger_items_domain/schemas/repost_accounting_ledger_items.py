"""Pydantic v2 schemas for RepostAccountingLedgerItems."""





from __future__ import annotations

from app.accounts.repost_accounting_ledger_items_domain.models.repost_accounting_ledger_items import (

    RepostAccountingLedgerItemsStatus,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "RepostAccountingLedgerItemsCreate",

    "RepostAccountingLedgerItemsRead",

    "RepostAccountingLedgerItemsListResponse",

]





class RepostAccountingLedgerItemsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    voucher_type: str

    voucher_no: Optional[str] = None

    status: Optional[RepostAccountingLedgerItemsStatus] = None

    traceback: Optional[str] = None





class RepostAccountingLedgerItemsCreate(RepostAccountingLedgerItemsBase):

    """Accepted only nested inside the parent payload."""

    pass





class RepostAccountingLedgerItemsRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    voucher_type: str

    voucher_no: Optional[str] = None

    status: Optional[RepostAccountingLedgerItemsStatus] = None

    traceback: Optional[str] = None





RepostAccountingLedgerItemsListResponse = Page[RepostAccountingLedgerItemsRead]

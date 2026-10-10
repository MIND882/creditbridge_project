"""Pydantic v2 schemas for RepostPaymentLedgerItems."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "RepostPaymentLedgerItemsCreate",

    "RepostPaymentLedgerItemsRead",

    "RepostPaymentLedgerItemsListResponse",

]





class RepostPaymentLedgerItemsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None





class RepostPaymentLedgerItemsCreate(RepostPaymentLedgerItemsBase):

    """Accepted only nested inside the parent payload."""

    pass





class RepostPaymentLedgerItemsRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None





RepostPaymentLedgerItemsListResponse = Page[RepostPaymentLedgerItemsRead]

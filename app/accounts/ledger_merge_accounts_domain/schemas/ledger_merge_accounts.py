"""Pydantic v2 schemas for LedgerMergeAccounts."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LedgerMergeAccountsCreate",

    "LedgerMergeAccountsRead",

    "LedgerMergeAccountsListResponse",

]





class LedgerMergeAccountsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    account_id: uuid.UUID

    merged: Optional[bool] = None

    account_name: str





class LedgerMergeAccountsCreate(LedgerMergeAccountsBase):

    """Accepted only nested inside the parent payload."""

    pass





class LedgerMergeAccountsRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    account_id: uuid.UUID

    merged: bool

    account_name: str





LedgerMergeAccountsListResponse = Page[LedgerMergeAccountsRead]

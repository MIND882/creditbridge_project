"""Pydantic v2 schemas for LedgerMerge."""





from __future__ import annotations

from app.accounts.ledger_merge_domain.models.ledger_merge import (

    LedgerMergeRootType,

    LedgerMergeStatus,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.ledger_merge_accounts_domain.schemas.ledger_merge_accounts import (

    LedgerMergeAccountsCreate,

    LedgerMergeAccountsRead,

)



__all__ = [

    "LedgerMergeCreate",

    "LedgerMergeUpdate",

    "LedgerMergeRead",

    "LedgerMergeListResponse",

]





class LedgerMergeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    account_id: uuid.UUID

    status: Optional[LedgerMergeStatus] = None

    root_type: LedgerMergeRootType

    account_name: str

    is_group: Optional[bool] = None



    merge_accounts: list[LedgerMergeAccountsCreate] = []





class LedgerMergeCreate(LedgerMergeBase):

    pass





class LedgerMergeUpdate(InputSchema):

    """A partial update."""



    account_id: Optional[uuid.UUID] = None

    status: Optional[LedgerMergeStatus] = None

    root_type: Optional[LedgerMergeRootType] = None

    account_name: Optional[str] = None

    is_group: Optional[bool] = None

    merge_accounts: Optional[list[LedgerMergeAccountsCreate]] = None





class LedgerMergeRead(ReadSchema):

    id: uuid.UUID

    name: str

    account_id: uuid.UUID

    status: Optional[LedgerMergeStatus] = None

    root_type: LedgerMergeRootType

    account_name: str

    is_group: bool

    merge_accounts: list[LedgerMergeAccountsRead] = []





LedgerMergeListResponse = Page[LedgerMergeRead]

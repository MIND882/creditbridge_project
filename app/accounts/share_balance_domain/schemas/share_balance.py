"""Pydantic v2 schemas for ShareBalance (child table, read-only API)."""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page

from app.accounts.share_balance_domain.models.share_balance import ShareCurrentState



__all__ = [

    "ShareBalanceCreate",

    "ShareBalanceRead",

    "ShareBalanceListResponse",

]





class ShareBalanceCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    share_type_id: uuid.UUID

    from_no: int

    to_no: int

    rate: Decimal

    no_of_shares: int

    amount: Optional[Decimal] = None

    is_company: Optional[bool] = False

    current_state: Optional[ShareCurrentState] = None





class ShareBalanceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    share_type_id: Optional[uuid.UUID] = None

    from_no: int

    to_no: int

    rate: Decimal

    no_of_shares: int

    amount: Decimal

    is_company: bool

    current_state: Optional[ShareCurrentState] = None





ShareBalanceListResponse = Page[ShareBalanceRead]

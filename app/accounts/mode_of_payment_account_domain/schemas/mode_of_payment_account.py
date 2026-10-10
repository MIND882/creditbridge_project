"""Pydantic v2 schemas for ModeOfPaymentAccount (child table, read-only API)."""



from __future__ import annotations



from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ModeOfPaymentAccountCreate",

    "ModeOfPaymentAccountRead",

    "ModeOfPaymentAccountListResponse",

]





class ModeOfPaymentAccountCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    company: Optional[str] = None

    default_account_id: Optional[uuid.UUID] = None





class ModeOfPaymentAccountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    company: Optional[str] = None

    default_account_id: Optional[uuid.UUID] = None





ModeOfPaymentAccountListResponse = Page[ModeOfPaymentAccountRead]

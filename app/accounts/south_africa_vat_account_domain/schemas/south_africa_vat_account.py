"""Pydantic v2 schemas for SouthAfricaVatAccount."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SouthAfricaVatAccountCreate",

    "SouthAfricaVatAccountRead",

    "SouthAfricaVatAccountListResponse",

]





class SouthAfricaVatAccountBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    account_id: Optional[uuid.UUID] = None





class SouthAfricaVatAccountCreate(SouthAfricaVatAccountBase):

    """Accepted only nested inside the parent payload."""

    pass





class SouthAfricaVatAccountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    account_id: Optional[uuid.UUID] = None





SouthAfricaVatAccountListResponse = Page[SouthAfricaVatAccountRead]

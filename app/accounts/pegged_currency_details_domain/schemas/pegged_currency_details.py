"""Pydantic v2 schemas for PeggedCurrencyDetails."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PeggedCurrencyDetailsCreate",

    "PeggedCurrencyDetailsRead",

    "PeggedCurrencyDetailsListResponse",

]





class PeggedCurrencyDetailsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    source_currency: Optional[str] = None

    pegged_exchange_rate: Optional[str] = None

    pegged_against: Optional[str] = None





class PeggedCurrencyDetailsCreate(PeggedCurrencyDetailsBase):

    """Accepted only nested inside the parent payload."""

    pass





class PeggedCurrencyDetailsRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    source_currency: Optional[str] = None

    pegged_exchange_rate: Optional[str] = None

    pegged_against: Optional[str] = None





PeggedCurrencyDetailsListResponse = Page[PeggedCurrencyDetailsRead]

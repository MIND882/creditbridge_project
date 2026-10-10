"""Pydantic v2 schemas for CurrencyExchangeSettingsResult."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CurrencyExchangeSettingsResultCreate",

    "CurrencyExchangeSettingsResultRead",

    "CurrencyExchangeSettingsResultListResponse",

]





class CurrencyExchangeSettingsResultBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    key: str





class CurrencyExchangeSettingsResultCreate(CurrencyExchangeSettingsResultBase):

    """Accepted only nested inside the parent payload."""

    pass





class CurrencyExchangeSettingsResultRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    key: str





CurrencyExchangeSettingsResultListResponse = Page[CurrencyExchangeSettingsResultRead]

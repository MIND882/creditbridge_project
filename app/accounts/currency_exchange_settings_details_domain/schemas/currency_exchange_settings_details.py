"""Pydantic v2 schemas for CurrencyExchangeSettingsDetails."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CurrencyExchangeSettingsDetailsCreate",

    "CurrencyExchangeSettingsDetailsRead",

    "CurrencyExchangeSettingsDetailsListResponse",

]





class CurrencyExchangeSettingsDetailsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    key: str

    value: str





class CurrencyExchangeSettingsDetailsCreate(CurrencyExchangeSettingsDetailsBase):

    """Accepted only nested inside the parent payload."""

    pass





class CurrencyExchangeSettingsDetailsRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    key: str

    value: str





CurrencyExchangeSettingsDetailsListResponse = Page[CurrencyExchangeSettingsDetailsRead]

"""Pydantic v2 schemas for CustomsTariffNumber."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CustomsTariffNumberCreate",

    "CustomsTariffNumberUpdate",

    "CustomsTariffNumberRead",

    "CustomsTariffNumberListResponse",

]





class CustomsTariffNumberBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    tariff_number: str

    description: Optional[str] = None





class CustomsTariffNumberCreate(CustomsTariffNumberBase):

    pass





class CustomsTariffNumberUpdate(InputSchema):

    """A partial update."""



    tariff_number: Optional[str] = None

    description: Optional[str] = None





class CustomsTariffNumberRead(ReadSchema):

    id: uuid.UUID

    name: str

    tariff_number: str

    description: Optional[str] = None





CustomsTariffNumberListResponse = Page[CustomsTariffNumberRead]

"""Pydantic v2 schemas for PriceListCountry."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PriceListCountryCreate",

    "PriceListCountryRead",

    "PriceListCountryListResponse",

]





class PriceListCountryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    country: str





class PriceListCountryCreate(PriceListCountryBase):

    pass





class PriceListCountryUpdate(InputSchema):

    """A partial update."""



    country: Optional[str] = None





class PriceListCountryRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    country: str





PriceListCountryListResponse = Page[PriceListCountryRead]

"""Pydantic v2 schemas for PriceList."""





from __future__ import annotations

from typing import Optional

import uuid



from app.stock.price_list_country_domain.schemas.price_list_country import (

    PriceListCountryCreate,

    PriceListCountryRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PriceListCreate",

    "PriceListUpdate",

    "PriceListRead",

    "PriceListListResponse",

]





class PriceListBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    enabled: Optional[bool] = None

    price_list_name: str

    currency: str

    buying: Optional[bool] = None

    selling: Optional[bool] = None

    price_not_uom_dependent: Optional[bool] = None

    countries: list[PriceListCountryCreate] = []





class PriceListCreate(PriceListBase):

    pass





class PriceListUpdate(InputSchema):

    """A partial update."""



    enabled: Optional[bool] = None

    price_list_name: Optional[str] = None

    currency: Optional[str] = None

    buying: Optional[bool] = None

    selling: Optional[bool] = None

    price_not_uom_dependent: Optional[bool] = None

    countries: Optional[list[PriceListCountryCreate]] = None





class PriceListRead(ReadSchema):

    id: uuid.UUID

    name: str

    enabled: Optional[bool] = None

    price_list_name: str

    currency: str

    buying: Optional[bool] = None

    selling: Optional[bool] = None

    price_not_uom_dependent: Optional[bool] = None

    countries: list[PriceListCountryRead] = []





PriceListListResponse = Page[PriceListRead]

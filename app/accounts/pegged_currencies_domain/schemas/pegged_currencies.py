"""Pydantic v2 schemas for PeggedCurrencies."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.pegged_currency_details_domain.schemas.pegged_currency_details import (

    PeggedCurrencyDetailsCreate,

    PeggedCurrencyDetailsRead,

)



__all__ = [

    "PeggedCurrenciesCreate",

    "PeggedCurrenciesUpdate",

    "PeggedCurrenciesRead",

    "PeggedCurrenciesListResponse",

]





class PeggedCurrenciesBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    pass



    pegged_currency_item: list[PeggedCurrencyDetailsCreate] = []





class PeggedCurrenciesCreate(PeggedCurrenciesBase):

    pass





class PeggedCurrenciesUpdate(InputSchema):

    """A partial update."""



    pass

    pegged_currency_item: Optional[list[PeggedCurrencyDetailsCreate]] = None





class PeggedCurrenciesRead(ReadSchema):

    id: uuid.UUID

    name: str

    pegged_currency_item: list[PeggedCurrencyDetailsRead] = []





PeggedCurrenciesListResponse = Page[PeggedCurrenciesRead]

"""Pydantic v2 schemas for CurrencyExchangeSettings."""





from __future__ import annotations

from app.accounts.currency_exchange_settings_domain.models.currency_exchange_settings import (

    CurrencyExchangeSettingsServiceProvider,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.currency_exchange_settings_details_domain.schemas.currency_exchange_settings_details import (

    CurrencyExchangeSettingsDetailsCreate,

    CurrencyExchangeSettingsDetailsRead,

)

from app.accounts.currency_exchange_settings_result_domain.schemas.currency_exchange_settings_result import (

    CurrencyExchangeSettingsResultCreate,

    CurrencyExchangeSettingsResultRead,

)



__all__ = [

    "CurrencyExchangeSettingsCreate",

    "CurrencyExchangeSettingsUpdate",

    "CurrencyExchangeSettingsRead",

    "CurrencyExchangeSettingsListResponse",

]





class CurrencyExchangeSettingsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    api_endpoint: str

    url: Optional[str] = None

    service_provider: CurrencyExchangeSettingsServiceProvider

    disabled: Optional[bool] = None

    access_key: Optional[str] = None

    use_http: Optional[bool] = None



    req_params: list[CurrencyExchangeSettingsDetailsCreate] = []



    result_key: list[CurrencyExchangeSettingsResultCreate] = []





class CurrencyExchangeSettingsCreate(CurrencyExchangeSettingsBase):

    pass





class CurrencyExchangeSettingsUpdate(InputSchema):

    """A partial update."""



    api_endpoint: Optional[str] = None

    url: Optional[str] = None

    service_provider: Optional[CurrencyExchangeSettingsServiceProvider] = None

    disabled: Optional[bool] = None

    access_key: Optional[str] = None

    use_http: Optional[bool] = None

    req_params: Optional[list[CurrencyExchangeSettingsDetailsCreate]] = None

    result_key: Optional[list[CurrencyExchangeSettingsResultCreate]] = None





class CurrencyExchangeSettingsRead(ReadSchema):

    id: uuid.UUID

    name: str

    api_endpoint: str

    url: Optional[str] = None

    service_provider: CurrencyExchangeSettingsServiceProvider

    disabled: bool

    access_key: Optional[str] = None

    use_http: bool

    req_params: list[CurrencyExchangeSettingsDetailsRead] = []

    result_key: list[CurrencyExchangeSettingsResultRead] = []





CurrencyExchangeSettingsListResponse = Page[CurrencyExchangeSettingsRead]

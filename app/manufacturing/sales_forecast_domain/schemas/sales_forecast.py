"""Pydantic v2 schemas for SalesForecast."""





from __future__ import annotations

from app.manufacturing.sales_forecast_domain.models.sales_forecast import (

    SalesForecastNamingSeries,

    SalesForecastFrequency,

    SalesForecastStatus,

)

from typing import Optional

import datetime as dt

import uuid



from app.manufacturing.sales_forecast_item_domain.schemas.sales_forecast_item import (

    SalesForecastItemCreate,

    SalesForecastItemRead,

)

from app.manufacturing.sales_forecast_item_domain.schemas.sales_forecast_item import (

    SalesForecastItemCreate,

    SalesForecastItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesForecastCreate",

    "SalesForecastUpdate",

    "SalesForecastRead",

    "SalesForecastListResponse",

]





class SalesForecastBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: SalesForecastNamingSeries

    company: str

    posting_date: Optional[dt.date] = None

    from_date: dt.date

    frequency: SalesForecastFrequency

    demand_number: int

    parent_warehouse_id: uuid.UUID

    amended_from_id: Optional[uuid.UUID] = None

    status: Optional[SalesForecastStatus] = None

    selected_items: list[SalesForecastItemCreate] = []

    items: list[SalesForecastItemCreate] = []





class SalesForecastCreate(SalesForecastBase):

    pass





class SalesForecastUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[SalesForecastNamingSeries] = None

    company: Optional[str] = None

    posting_date: Optional[dt.date] = None

    from_date: Optional[dt.date] = None

    frequency: Optional[SalesForecastFrequency] = None

    demand_number: Optional[int] = None

    parent_warehouse_id: Optional[uuid.UUID] = None

    amended_from_id: Optional[uuid.UUID] = None

    status: Optional[SalesForecastStatus] = None

    selected_items: Optional[list[SalesForecastItemCreate]] = None

    items: Optional[list[SalesForecastItemCreate]] = None





class SalesForecastRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[SalesForecastNamingSeries] = None

    company: str

    posting_date: Optional[dt.date] = None

    from_date: Optional[dt.date] = None

    frequency: Optional[SalesForecastFrequency] = None

    demand_number: Optional[int] = None

    parent_warehouse_id: Optional[uuid.UUID] = None

    amended_from_id: Optional[uuid.UUID] = None

    status: Optional[SalesForecastStatus] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    selected_items: list[SalesForecastItemRead] = []

    items: list[SalesForecastItemRead] = []





SalesForecastListResponse = Page[SalesForecastRead]

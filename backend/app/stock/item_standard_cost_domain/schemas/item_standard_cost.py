"""Pydantic v2 schemas for ItemStandardCost."""





from __future__ import annotations

from app.stock.item_standard_cost_domain.models.item_standard_cost import (

    ItemStandardCostNamingSeries,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemStandardCostCreate",

    "ItemStandardCostUpdate",

    "ItemStandardCostRead",

    "ItemStandardCostListResponse",

]





class ItemStandardCostBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: ItemStandardCostNamingSeries

    item_code_id: uuid.UUID

    company: str

    standard_rate: Decimal

    effective_date: dt.date

    revaluation_entry_id: Optional[uuid.UUID] = None

    amended_from_id: Optional[uuid.UUID] = None





class ItemStandardCostCreate(ItemStandardCostBase):

    pass





class ItemStandardCostUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[ItemStandardCostNamingSeries] = None

    item_code_id: Optional[uuid.UUID] = None

    company: Optional[str] = None

    standard_rate: Optional[Decimal] = None

    effective_date: Optional[dt.date] = None

    revaluation_entry_id: Optional[uuid.UUID] = None

    amended_from_id: Optional[uuid.UUID] = None





class ItemStandardCostRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[ItemStandardCostNamingSeries] = None

    item_code_id: Optional[uuid.UUID] = None

    company: str

    standard_rate: Optional[Decimal] = None

    effective_date: Optional[dt.date] = None

    revaluation_entry_id: Optional[uuid.UUID] = None

    amended_from_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





ItemStandardCostListResponse = Page[ItemStandardCostRead]

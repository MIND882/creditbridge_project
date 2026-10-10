"""Pydantic v2 schemas for ItemLeadTime."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemLeadTimeCreate",

    "ItemLeadTimeUpdate",

    "ItemLeadTimeRead",

    "ItemLeadTimeListResponse",

]





class ItemLeadTimeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    buffer_time: Optional[int] = None

    no_of_shift: Optional[int] = None

    manufacturing_time_in_mins: Optional[int] = None

    total_workstation_time: Optional[int] = None

    daily_yield: Optional[Decimal] = None

    capacity_per_day: Optional[int] = None

    no_of_units_produced: Optional[int] = None

    purchase_time: Optional[int] = None

    shift_time_in_hours: Optional[int] = None

    no_of_workstations: Optional[int] = None

    stock_uom_id: Optional[uuid.UUID] = None





class ItemLeadTimeCreate(ItemLeadTimeBase):

    pass





class ItemLeadTimeUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    buffer_time: Optional[int] = None

    no_of_shift: Optional[int] = None

    manufacturing_time_in_mins: Optional[int] = None

    total_workstation_time: Optional[int] = None

    daily_yield: Optional[Decimal] = None

    capacity_per_day: Optional[int] = None

    no_of_units_produced: Optional[int] = None

    purchase_time: Optional[int] = None

    shift_time_in_hours: Optional[int] = None

    no_of_workstations: Optional[int] = None

    stock_uom_id: Optional[uuid.UUID] = None





class ItemLeadTimeRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    buffer_time: Optional[int] = None

    no_of_shift: Optional[int] = None

    manufacturing_time_in_mins: Optional[int] = None

    total_workstation_time: Optional[int] = None

    daily_yield: Optional[Decimal] = None

    capacity_per_day: Optional[int] = None

    no_of_units_produced: Optional[int] = None

    purchase_time: Optional[int] = None

    shift_time_in_hours: Optional[int] = None

    no_of_workstations: Optional[int] = None

    stock_uom_id: Optional[uuid.UUID] = None





ItemLeadTimeListResponse = Page[ItemLeadTimeRead]

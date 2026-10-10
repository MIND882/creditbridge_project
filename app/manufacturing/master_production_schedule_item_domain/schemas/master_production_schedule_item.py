"""Pydantic v2 schemas for MasterProductionScheduleItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "MasterProductionScheduleItemCreate",

    "MasterProductionScheduleItemRead",

    "MasterProductionScheduleItemListResponse",

]





class MasterProductionScheduleItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    delivery_date: Optional[dt.date] = None

    cumulative_lead_time: Optional[int] = None

    order_release_date: Optional[dt.date] = None

    planned_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    bom_no_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None





class MasterProductionScheduleItemCreate(MasterProductionScheduleItemBase):

    pass





class MasterProductionScheduleItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    delivery_date: Optional[dt.date] = None

    cumulative_lead_time: Optional[int] = None

    order_release_date: Optional[dt.date] = None

    planned_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    bom_no_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None





class MasterProductionScheduleItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    delivery_date: Optional[dt.date] = None

    cumulative_lead_time: Optional[int] = None

    order_release_date: Optional[dt.date] = None

    planned_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    bom_no_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None





MasterProductionScheduleItemListResponse = Page[MasterProductionScheduleItemRead]

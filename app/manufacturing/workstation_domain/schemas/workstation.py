"""Pydantic v2 schemas for Workstation."""





from __future__ import annotations

from app.manufacturing.workstation_domain.models.workstation import (

    WorkstationStatus,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.manufacturing.workstation_cost_domain.schemas.workstation_cost import (

    WorkstationCostCreate,

    WorkstationCostRead,

)

from app.manufacturing.workstation_working_hour_domain.schemas.workstation_working_hour import (

    WorkstationWorkingHourCreate,

    WorkstationWorkingHourRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WorkstationCreate",

    "WorkstationUpdate",

    "WorkstationRead",

    "WorkstationListResponse",

]





class WorkstationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    workstation_name: Optional[str] = None

    workstation_type_id: Optional[uuid.UUID] = None

    plant_floor_id: Optional[uuid.UUID] = None

    disabled: Optional[bool] = None

    production_capacity: int

    warehouse_id: Optional[uuid.UUID] = None

    status: Optional[WorkstationStatus] = None

    on_status_image: Optional[str] = None

    off_status_image: Optional[str] = None

    hour_rate: Optional[Decimal] = None

    description: Optional[str] = None

    holiday_list: Optional[str] = None

    total_working_hours: Optional[Decimal] = None

    workstation_costs: list[WorkstationCostCreate] = []

    working_hours: list[WorkstationWorkingHourCreate] = []





class WorkstationCreate(WorkstationBase):

    pass





class WorkstationUpdate(InputSchema):

    """A partial update."""



    workstation_name: Optional[str] = None

    workstation_type_id: Optional[uuid.UUID] = None

    plant_floor_id: Optional[uuid.UUID] = None

    disabled: Optional[bool] = None

    production_capacity: Optional[int] = None

    warehouse_id: Optional[uuid.UUID] = None

    status: Optional[WorkstationStatus] = None

    on_status_image: Optional[str] = None

    off_status_image: Optional[str] = None

    hour_rate: Optional[Decimal] = None

    description: Optional[str] = None

    holiday_list: Optional[str] = None

    total_working_hours: Optional[Decimal] = None

    workstation_costs: Optional[list[WorkstationCostCreate]] = None

    working_hours: Optional[list[WorkstationWorkingHourCreate]] = None





class WorkstationRead(ReadSchema):

    id: uuid.UUID

    name: str

    workstation_name: Optional[str] = None

    workstation_type_id: Optional[uuid.UUID] = None

    plant_floor_id: Optional[uuid.UUID] = None

    disabled: Optional[bool] = None

    production_capacity: Optional[int] = None

    warehouse_id: Optional[uuid.UUID] = None

    status: Optional[WorkstationStatus] = None

    on_status_image: Optional[str] = None

    off_status_image: Optional[str] = None

    hour_rate: Optional[Decimal] = None

    description: Optional[str] = None

    holiday_list: Optional[str] = None

    total_working_hours: Optional[Decimal] = None

    workstation_costs: list[WorkstationCostRead] = []

    working_hours: list[WorkstationWorkingHourRead] = []





WorkstationListResponse = Page[WorkstationRead]

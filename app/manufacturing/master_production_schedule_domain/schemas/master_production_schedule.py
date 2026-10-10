"""Pydantic v2 schemas for MasterProductionSchedule."""





from __future__ import annotations

from app.manufacturing.master_production_schedule_domain.models.master_production_schedule import (

    MasterProductionScheduleNamingSeries,

)

from typing import Optional

import datetime as dt

import uuid



from app.manufacturing.production_plan_sales_order_domain.schemas.production_plan_sales_order import (

    ProductionPlanSalesOrderCreate,

    ProductionPlanSalesOrderRead,

)

from app.manufacturing.production_plan_material_request_domain.schemas.production_plan_material_request import (

    ProductionPlanMaterialRequestCreate,

    ProductionPlanMaterialRequestRead,

)

from app.manufacturing.master_production_schedule_item_domain.schemas.master_production_schedule_item import (

    MasterProductionScheduleItemCreate,

    MasterProductionScheduleItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "MasterProductionScheduleCreate",

    "MasterProductionScheduleUpdate",

    "MasterProductionScheduleRead",

    "MasterProductionScheduleListResponse",

]





class MasterProductionScheduleBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: MasterProductionScheduleNamingSeries

    company: str

    posting_date: dt.date

    from_date: dt.date

    to_date: Optional[dt.date] = None

    parent_warehouse_id: Optional[uuid.UUID] = None

    sales_forecast_id: Optional[uuid.UUID] = None

    amended_from_id: Optional[uuid.UUID] = None

    sales_orders: list[ProductionPlanSalesOrderCreate] = []

    material_requests: list[ProductionPlanMaterialRequestCreate] = []

    items: list[MasterProductionScheduleItemCreate] = []





class MasterProductionScheduleCreate(MasterProductionScheduleBase):

    pass





class MasterProductionScheduleUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[MasterProductionScheduleNamingSeries] = None

    company: Optional[str] = None

    posting_date: Optional[dt.date] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    parent_warehouse_id: Optional[uuid.UUID] = None

    sales_forecast_id: Optional[uuid.UUID] = None

    amended_from_id: Optional[uuid.UUID] = None

    sales_orders: Optional[list[ProductionPlanSalesOrderCreate]] = None

    material_requests: Optional[list[ProductionPlanMaterialRequestCreate]] = None

    items: Optional[list[MasterProductionScheduleItemCreate]] = None





class MasterProductionScheduleRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[MasterProductionScheduleNamingSeries] = None

    company: str

    posting_date: Optional[dt.date] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    parent_warehouse_id: Optional[uuid.UUID] = None

    sales_forecast_id: Optional[uuid.UUID] = None

    amended_from_id: Optional[uuid.UUID] = None

    sales_orders: list[ProductionPlanSalesOrderRead] = []

    material_requests: list[ProductionPlanMaterialRequestRead] = []

    items: list[MasterProductionScheduleItemRead] = []





MasterProductionScheduleListResponse = Page[MasterProductionScheduleRead]

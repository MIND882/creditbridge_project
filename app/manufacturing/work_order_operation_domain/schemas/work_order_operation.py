"""Pydantic v2 schemas for WorkOrderOperation."""





from __future__ import annotations

from app.manufacturing.work_order_operation_domain.models.work_order_operation import (

    WorkOrderOperationStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WorkOrderOperationCreate",

    "WorkOrderOperationRead",

    "WorkOrderOperationListResponse",

]





class WorkOrderOperationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    operation_id: uuid.UUID

    status: Optional[WorkOrderOperationStatus] = None

    completed_qty: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    pending_qty: Optional[Decimal] = None

    bom_id: Optional[uuid.UUID] = None

    workstation_type_id: Optional[uuid.UUID] = None

    workstation_id: Optional[uuid.UUID] = None

    sequence_id: Optional[int] = None

    quality_inspection_required: Optional[bool] = None

    bom_no_id: Optional[uuid.UUID] = None

    finished_good_id: Optional[uuid.UUID] = None

    is_subcontracted: Optional[bool] = None

    skip_material_transfer: Optional[bool] = None

    backflush_from_wip_warehouse: Optional[bool] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    planned_start_time: Optional[dt.datetime] = None

    hour_rate: Optional[Decimal] = None

    time_in_mins: Decimal

    planned_end_time: Optional[dt.datetime] = None

    batch_size: Optional[Decimal] = None

    planned_operating_cost: Optional[Decimal] = None

    actual_start_time: Optional[dt.datetime] = None

    actual_operation_time: Optional[Decimal] = None

    actual_end_time: Optional[dt.datetime] = None

    actual_operating_cost: Optional[Decimal] = None





class WorkOrderOperationCreate(WorkOrderOperationBase):

    pass





class WorkOrderOperationUpdate(InputSchema):

    """A partial update."""



    operation_id: Optional[uuid.UUID] = None

    status: Optional[WorkOrderOperationStatus] = None

    completed_qty: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    pending_qty: Optional[Decimal] = None

    bom_id: Optional[uuid.UUID] = None

    workstation_type_id: Optional[uuid.UUID] = None

    workstation_id: Optional[uuid.UUID] = None

    sequence_id: Optional[int] = None

    quality_inspection_required: Optional[bool] = None

    bom_no_id: Optional[uuid.UUID] = None

    finished_good_id: Optional[uuid.UUID] = None

    is_subcontracted: Optional[bool] = None

    skip_material_transfer: Optional[bool] = None

    backflush_from_wip_warehouse: Optional[bool] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    planned_start_time: Optional[dt.datetime] = None

    hour_rate: Optional[Decimal] = None

    time_in_mins: Optional[Decimal] = None

    planned_end_time: Optional[dt.datetime] = None

    batch_size: Optional[Decimal] = None

    planned_operating_cost: Optional[Decimal] = None

    actual_start_time: Optional[dt.datetime] = None

    actual_operation_time: Optional[Decimal] = None

    actual_end_time: Optional[dt.datetime] = None

    actual_operating_cost: Optional[Decimal] = None





class WorkOrderOperationRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    operation_id: Optional[uuid.UUID] = None

    status: Optional[WorkOrderOperationStatus] = None

    completed_qty: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    pending_qty: Optional[Decimal] = None

    bom_id: Optional[uuid.UUID] = None

    workstation_type_id: Optional[uuid.UUID] = None

    workstation_id: Optional[uuid.UUID] = None

    sequence_id: Optional[int] = None

    quality_inspection_required: Optional[bool] = None

    bom_no_id: Optional[uuid.UUID] = None

    finished_good_id: Optional[uuid.UUID] = None

    is_subcontracted: Optional[bool] = None

    skip_material_transfer: Optional[bool] = None

    backflush_from_wip_warehouse: Optional[bool] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    planned_start_time: Optional[dt.datetime] = None

    hour_rate: Optional[Decimal] = None

    time_in_mins: Optional[Decimal] = None

    planned_end_time: Optional[dt.datetime] = None

    batch_size: Optional[Decimal] = None

    planned_operating_cost: Optional[Decimal] = None

    actual_start_time: Optional[dt.datetime] = None

    actual_operation_time: Optional[Decimal] = None

    actual_end_time: Optional[dt.datetime] = None

    actual_operating_cost: Optional[Decimal] = None





WorkOrderOperationListResponse = Page[WorkOrderOperationRead]

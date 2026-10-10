"""Pydantic v2 schemas for WorkOrder."""





from __future__ import annotations

from app.manufacturing.work_order_domain.models.work_order import (

    WorkOrderNamingSeries,

    WorkOrderTransferMaterialAgainst,

    WorkOrderStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.manufacturing.work_order_operation_domain.schemas.work_order_operation import (

    WorkOrderOperationCreate,

    WorkOrderOperationRead,

)

from app.manufacturing.work_order_item_domain.schemas.work_order_item import (

    WorkOrderItemCreate,

    WorkOrderItemRead,

)

from app.manufacturing.work_order_additional_item_domain.schemas.work_order_additional_item import (

    WorkOrderAdditionalItemCreate,

    WorkOrderAdditionalItemRead,

)

from app.manufacturing.work_order_additional_item_domain.schemas.work_order_additional_item import (

    WorkOrderAdditionalItemCreate,

    WorkOrderAdditionalItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WorkOrderCreate",

    "WorkOrderUpdate",

    "WorkOrderRead",

    "WorkOrderListResponse",

]





class WorkOrderBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    company: str

    naming_series: WorkOrderNamingSeries

    production_item_id: uuid.UUID

    bom_no_id: uuid.UUID

    qty: Decimal

    sales_order_id: Optional[uuid.UUID] = None

    reserve_stock: Optional[bool] = None

    max_producible_qty: Optional[Decimal] = None

    material_transferred_for_manufacturing: Optional[Decimal] = None

    additional_transferred_qty: Optional[Decimal] = None

    produced_qty: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    disassembled_qty: Optional[Decimal] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    scrap_warehouse_id: Optional[uuid.UUID] = None

    transfer_material_against: Optional[WorkOrderTransferMaterialAgainst] = None

    allow_alternative_item: Optional[bool] = None

    use_multi_level_bom: Optional[bool] = None

    skip_transfer: Optional[bool] = None

    from_wip_warehouse: Optional[bool] = None

    update_consumed_material_cost_in_project: Optional[bool] = None

    planned_start_date: dt.datetime

    planned_end_date: Optional[dt.datetime] = None

    expected_delivery_date: Optional[dt.date] = None

    actual_start_date: Optional[dt.datetime] = None

    actual_end_date: Optional[dt.datetime] = None

    lead_time: Optional[Decimal] = None

    planned_operating_cost: Optional[Decimal] = None

    actual_operating_cost: Optional[Decimal] = None

    additional_operating_cost: Optional[Decimal] = None

    corrective_operation_cost: Optional[Decimal] = None

    total_operating_cost: Optional[Decimal] = None

    image: Optional[str] = None

    item_name: Optional[str] = None

    stock_uom_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    has_serial_no: Optional[bool] = None

    has_batch_no: Optional[bool] = None

    batch_size: Optional[Decimal] = None

    project: Optional[str] = None

    subcontracting_inward_order: Optional[str] = None

    production_plan_id: Optional[uuid.UUID] = None

    mps_id: Optional[uuid.UUID] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    subcontracting_inward_order_item: Optional[str] = None

    sales_order_item: Optional[str] = None

    production_plan_sub_assembly_item: Optional[str] = None

    production_plan_item: Optional[str] = None

    product_bundle_item_id: Optional[uuid.UUID] = None

    status: WorkOrderStatus

    track_semi_finished_goods: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    operations: list[WorkOrderOperationCreate] = []

    required_items: list[WorkOrderItemCreate] = []

    non_stock_items: list[WorkOrderAdditionalItemCreate] = []

    secondary_items: list[WorkOrderAdditionalItemCreate] = []





class WorkOrderCreate(WorkOrderBase):

    pass





class WorkOrderUpdate(InputSchema):

    """A partial update."""



    company: Optional[str] = None

    naming_series: Optional[WorkOrderNamingSeries] = None

    production_item_id: Optional[uuid.UUID] = None

    bom_no_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    sales_order_id: Optional[uuid.UUID] = None

    reserve_stock: Optional[bool] = None

    max_producible_qty: Optional[Decimal] = None

    material_transferred_for_manufacturing: Optional[Decimal] = None

    additional_transferred_qty: Optional[Decimal] = None

    produced_qty: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    disassembled_qty: Optional[Decimal] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    scrap_warehouse_id: Optional[uuid.UUID] = None

    transfer_material_against: Optional[WorkOrderTransferMaterialAgainst] = None

    allow_alternative_item: Optional[bool] = None

    use_multi_level_bom: Optional[bool] = None

    skip_transfer: Optional[bool] = None

    from_wip_warehouse: Optional[bool] = None

    update_consumed_material_cost_in_project: Optional[bool] = None

    planned_start_date: Optional[dt.datetime] = None

    planned_end_date: Optional[dt.datetime] = None

    expected_delivery_date: Optional[dt.date] = None

    actual_start_date: Optional[dt.datetime] = None

    actual_end_date: Optional[dt.datetime] = None

    lead_time: Optional[Decimal] = None

    planned_operating_cost: Optional[Decimal] = None

    actual_operating_cost: Optional[Decimal] = None

    additional_operating_cost: Optional[Decimal] = None

    corrective_operation_cost: Optional[Decimal] = None

    total_operating_cost: Optional[Decimal] = None

    image: Optional[str] = None

    item_name: Optional[str] = None

    stock_uom_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    has_serial_no: Optional[bool] = None

    has_batch_no: Optional[bool] = None

    batch_size: Optional[Decimal] = None

    project: Optional[str] = None

    subcontracting_inward_order: Optional[str] = None

    production_plan_id: Optional[uuid.UUID] = None

    mps_id: Optional[uuid.UUID] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    subcontracting_inward_order_item: Optional[str] = None

    sales_order_item: Optional[str] = None

    production_plan_sub_assembly_item: Optional[str] = None

    production_plan_item: Optional[str] = None

    product_bundle_item_id: Optional[uuid.UUID] = None

    status: Optional[WorkOrderStatus] = None

    track_semi_finished_goods: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    operations: Optional[list[WorkOrderOperationCreate]] = None

    required_items: Optional[list[WorkOrderItemCreate]] = None

    non_stock_items: Optional[list[WorkOrderAdditionalItemCreate]] = None

    secondary_items: Optional[list[WorkOrderAdditionalItemCreate]] = None





class WorkOrderRead(ReadSchema):

    id: uuid.UUID

    name: str

    company: str

    naming_series: Optional[WorkOrderNamingSeries] = None

    production_item_id: Optional[uuid.UUID] = None

    bom_no_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    sales_order_id: Optional[uuid.UUID] = None

    reserve_stock: Optional[bool] = None

    max_producible_qty: Optional[Decimal] = None

    material_transferred_for_manufacturing: Optional[Decimal] = None

    additional_transferred_qty: Optional[Decimal] = None

    produced_qty: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    disassembled_qty: Optional[Decimal] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    scrap_warehouse_id: Optional[uuid.UUID] = None

    transfer_material_against: Optional[WorkOrderTransferMaterialAgainst] = None

    allow_alternative_item: Optional[bool] = None

    use_multi_level_bom: Optional[bool] = None

    skip_transfer: Optional[bool] = None

    from_wip_warehouse: Optional[bool] = None

    update_consumed_material_cost_in_project: Optional[bool] = None

    planned_start_date: Optional[dt.datetime] = None

    planned_end_date: Optional[dt.datetime] = None

    expected_delivery_date: Optional[dt.date] = None

    actual_start_date: Optional[dt.datetime] = None

    actual_end_date: Optional[dt.datetime] = None

    lead_time: Optional[Decimal] = None

    planned_operating_cost: Optional[Decimal] = None

    actual_operating_cost: Optional[Decimal] = None

    additional_operating_cost: Optional[Decimal] = None

    corrective_operation_cost: Optional[Decimal] = None

    total_operating_cost: Optional[Decimal] = None

    image: Optional[str] = None

    item_name: Optional[str] = None

    stock_uom_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    has_serial_no: Optional[bool] = None

    has_batch_no: Optional[bool] = None

    batch_size: Optional[Decimal] = None

    project: Optional[str] = None

    subcontracting_inward_order: Optional[str] = None

    production_plan_id: Optional[uuid.UUID] = None

    mps_id: Optional[uuid.UUID] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    subcontracting_inward_order_item: Optional[str] = None

    sales_order_item: Optional[str] = None

    production_plan_sub_assembly_item: Optional[str] = None

    production_plan_item: Optional[str] = None

    product_bundle_item_id: Optional[uuid.UUID] = None

    status: Optional[WorkOrderStatus] = None

    track_semi_finished_goods: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    operations: list[WorkOrderOperationRead] = []

    required_items: list[WorkOrderItemRead] = []

    non_stock_items: list[WorkOrderAdditionalItemRead] = []

    secondary_items: list[WorkOrderAdditionalItemRead] = []





WorkOrderListResponse = Page[WorkOrderRead]

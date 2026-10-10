"""Pydantic v2 schemas for JobCard."""





from __future__ import annotations

from app.manufacturing.job_card_domain.models.job_card import (

    JobCardNamingSeries,

    JobCardStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.manufacturing.job_card_item_domain.schemas.job_card_item import (

    JobCardItemCreate,

    JobCardItemRead,

)

from app.manufacturing.job_card_scheduled_time_domain.schemas.job_card_scheduled_time import (

    JobCardScheduledTimeCreate,

    JobCardScheduledTimeRead,

)

from app.manufacturing.job_card_time_log_domain.schemas.job_card_time_log import (

    JobCardTimeLogCreate,

    JobCardTimeLogRead,

)

from app.manufacturing.job_card_operation_domain.schemas.job_card_operation import (

    JobCardOperationCreate,

    JobCardOperationRead,

)

from app.manufacturing.job_card_secondary_item_domain.schemas.job_card_secondary_item import (

    JobCardSecondaryItemCreate,

    JobCardSecondaryItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "JobCardCreate",

    "JobCardUpdate",

    "JobCardRead",

    "JobCardListResponse",

]





class JobCardBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    work_order_id: uuid.UUID

    production_item_id: Optional[uuid.UUID] = None

    bom_no_id: Optional[uuid.UUID] = None

    for_quantity: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    company: str

    naming_series: JobCardNamingSeries

    posting_date: Optional[dt.date] = None

    finished_good_id: Optional[uuid.UUID] = None

    semi_fg_bom_id: Optional[uuid.UUID] = None

    pending_qty: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    total_completed_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    manufactured_qty: Optional[Decimal] = None

    operation_id: uuid.UUID

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    skip_material_transfer: Optional[bool] = None

    backflush_from_wip_warehouse: Optional[bool] = None

    workstation_type_id: Optional[uuid.UUID] = None

    workstation_id: uuid.UUID

    target_warehouse_id: Optional[uuid.UUID] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    expected_start_date: Optional[dt.datetime] = None

    time_required: Optional[Decimal] = None

    expected_end_date: Optional[dt.datetime] = None

    actual_start_date: Optional[dt.datetime] = None

    total_time_in_mins: Optional[Decimal] = None

    actual_end_date: Optional[dt.datetime] = None

    for_job_card_id: Optional[uuid.UUID] = None

    is_corrective_job_card: Optional[bool] = None

    hour_rate: Optional[Decimal] = None

    for_operation_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    requested_qty: Optional[Decimal] = None

    is_paused: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    track_semi_finished_goods: Optional[bool] = None

    project: Optional[str] = None

    remarks: Optional[str] = None

    status: Optional[JobCardStatus] = None

    operation_row_id: Optional[int] = None

    amended_from_id: Optional[uuid.UUID] = None

    sequence_id: Optional[int] = None

    serial_no: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    items: list[JobCardItemCreate] = []

    scheduled_time_logs: list[JobCardScheduledTimeCreate] = []

    time_logs: list[JobCardTimeLogCreate] = []

    sub_operations: list[JobCardOperationCreate] = []

    secondary_items: list[JobCardSecondaryItemCreate] = []





class JobCardCreate(JobCardBase):

    pass





class JobCardUpdate(InputSchema):

    """A partial update."""



    work_order_id: Optional[uuid.UUID] = None

    production_item_id: Optional[uuid.UUID] = None

    bom_no_id: Optional[uuid.UUID] = None

    for_quantity: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    company: Optional[str] = None

    naming_series: Optional[JobCardNamingSeries] = None

    posting_date: Optional[dt.date] = None

    finished_good_id: Optional[uuid.UUID] = None

    semi_fg_bom_id: Optional[uuid.UUID] = None

    pending_qty: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    total_completed_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    manufactured_qty: Optional[Decimal] = None

    operation_id: Optional[uuid.UUID] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    skip_material_transfer: Optional[bool] = None

    backflush_from_wip_warehouse: Optional[bool] = None

    workstation_type_id: Optional[uuid.UUID] = None

    workstation_id: Optional[uuid.UUID] = None

    target_warehouse_id: Optional[uuid.UUID] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    expected_start_date: Optional[dt.datetime] = None

    time_required: Optional[Decimal] = None

    expected_end_date: Optional[dt.datetime] = None

    actual_start_date: Optional[dt.datetime] = None

    total_time_in_mins: Optional[Decimal] = None

    actual_end_date: Optional[dt.datetime] = None

    for_job_card_id: Optional[uuid.UUID] = None

    is_corrective_job_card: Optional[bool] = None

    hour_rate: Optional[Decimal] = None

    for_operation_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    requested_qty: Optional[Decimal] = None

    is_paused: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    track_semi_finished_goods: Optional[bool] = None

    project: Optional[str] = None

    remarks: Optional[str] = None

    status: Optional[JobCardStatus] = None

    operation_row_id: Optional[int] = None

    amended_from_id: Optional[uuid.UUID] = None

    sequence_id: Optional[int] = None

    serial_no: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    items: Optional[list[JobCardItemCreate]] = None

    scheduled_time_logs: Optional[list[JobCardScheduledTimeCreate]] = None

    time_logs: Optional[list[JobCardTimeLogCreate]] = None

    sub_operations: Optional[list[JobCardOperationCreate]] = None

    secondary_items: Optional[list[JobCardSecondaryItemCreate]] = None





class JobCardRead(ReadSchema):

    id: uuid.UUID

    name: str

    work_order_id: Optional[uuid.UUID] = None

    production_item_id: Optional[uuid.UUID] = None

    bom_no_id: Optional[uuid.UUID] = None

    for_quantity: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    company: str

    naming_series: Optional[JobCardNamingSeries] = None

    posting_date: Optional[dt.date] = None

    finished_good_id: Optional[uuid.UUID] = None

    semi_fg_bom_id: Optional[uuid.UUID] = None

    pending_qty: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    total_completed_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    manufactured_qty: Optional[Decimal] = None

    operation_id: Optional[uuid.UUID] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    skip_material_transfer: Optional[bool] = None

    backflush_from_wip_warehouse: Optional[bool] = None

    workstation_type_id: Optional[uuid.UUID] = None

    workstation_id: Optional[uuid.UUID] = None

    target_warehouse_id: Optional[uuid.UUID] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    expected_start_date: Optional[dt.datetime] = None

    time_required: Optional[Decimal] = None

    expected_end_date: Optional[dt.datetime] = None

    actual_start_date: Optional[dt.datetime] = None

    total_time_in_mins: Optional[Decimal] = None

    actual_end_date: Optional[dt.datetime] = None

    for_job_card_id: Optional[uuid.UUID] = None

    is_corrective_job_card: Optional[bool] = None

    hour_rate: Optional[Decimal] = None

    for_operation_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    requested_qty: Optional[Decimal] = None

    is_paused: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    track_semi_finished_goods: Optional[bool] = None

    project: Optional[str] = None

    remarks: Optional[str] = None

    status: Optional[JobCardStatus] = None

    operation_row_id: Optional[int] = None

    amended_from_id: Optional[uuid.UUID] = None

    sequence_id: Optional[int] = None

    serial_no: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[JobCardItemRead] = []

    scheduled_time_logs: list[JobCardScheduledTimeRead] = []

    time_logs: list[JobCardTimeLogRead] = []

    sub_operations: list[JobCardOperationRead] = []

    secondary_items: list[JobCardSecondaryItemRead] = []





JobCardListResponse = Page[JobCardRead]

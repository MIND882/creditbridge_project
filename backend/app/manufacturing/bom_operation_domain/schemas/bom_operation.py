"""Pydantic v2 schemas for BomOperation."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomOperationCreate",

    "BomOperationRead",

    "BomOperationListResponse",

]





class BomOperationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    operation_id: uuid.UUID

    sequence_id: Optional[int] = None

    finished_good_id: Optional[uuid.UUID] = None

    finished_good_qty: Optional[Decimal] = None

    bom_no_id: Optional[uuid.UUID] = None

    workstation_type_id: Optional[uuid.UUID] = None

    workstation_id: Optional[uuid.UUID] = None

    time_in_mins: Decimal

    fixed_time: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    is_final_finished_good: Optional[bool] = None

    set_cost_based_on_bom_qty: Optional[bool] = None

    quality_inspection_required: Optional[bool] = None

    skip_material_transfer: Optional[bool] = None

    backflush_from_wip_warehouse: Optional[bool] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    hour_rate: Optional[Decimal] = None

    base_hour_rate: Optional[Decimal] = None

    batch_size: Optional[Decimal] = None

    cost_per_unit: Optional[Decimal] = None

    base_cost_per_unit: Optional[Decimal] = None

    operating_cost: Optional[Decimal] = None

    base_operating_cost: Optional[Decimal] = None

    description: Optional[str] = None

    image: Optional[str] = None





class BomOperationCreate(BomOperationBase):

    pass





class BomOperationUpdate(InputSchema):

    """A partial update."""



    operation_id: Optional[uuid.UUID] = None

    sequence_id: Optional[int] = None

    finished_good_id: Optional[uuid.UUID] = None

    finished_good_qty: Optional[Decimal] = None

    bom_no_id: Optional[uuid.UUID] = None

    workstation_type_id: Optional[uuid.UUID] = None

    workstation_id: Optional[uuid.UUID] = None

    time_in_mins: Optional[Decimal] = None

    fixed_time: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    is_final_finished_good: Optional[bool] = None

    set_cost_based_on_bom_qty: Optional[bool] = None

    quality_inspection_required: Optional[bool] = None

    skip_material_transfer: Optional[bool] = None

    backflush_from_wip_warehouse: Optional[bool] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    hour_rate: Optional[Decimal] = None

    base_hour_rate: Optional[Decimal] = None

    batch_size: Optional[Decimal] = None

    cost_per_unit: Optional[Decimal] = None

    base_cost_per_unit: Optional[Decimal] = None

    operating_cost: Optional[Decimal] = None

    base_operating_cost: Optional[Decimal] = None

    description: Optional[str] = None

    image: Optional[str] = None





class BomOperationRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    operation_id: Optional[uuid.UUID] = None

    sequence_id: Optional[int] = None

    finished_good_id: Optional[uuid.UUID] = None

    finished_good_qty: Optional[Decimal] = None

    bom_no_id: Optional[uuid.UUID] = None

    workstation_type_id: Optional[uuid.UUID] = None

    workstation_id: Optional[uuid.UUID] = None

    time_in_mins: Optional[Decimal] = None

    fixed_time: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    is_final_finished_good: Optional[bool] = None

    set_cost_based_on_bom_qty: Optional[bool] = None

    quality_inspection_required: Optional[bool] = None

    skip_material_transfer: Optional[bool] = None

    backflush_from_wip_warehouse: Optional[bool] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    wip_warehouse_id: Optional[uuid.UUID] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    hour_rate: Optional[Decimal] = None

    base_hour_rate: Optional[Decimal] = None

    batch_size: Optional[Decimal] = None

    cost_per_unit: Optional[Decimal] = None

    base_cost_per_unit: Optional[Decimal] = None

    operating_cost: Optional[Decimal] = None

    base_operating_cost: Optional[Decimal] = None

    description: Optional[str] = None

    image: Optional[str] = None





BomOperationListResponse = Page[BomOperationRead]

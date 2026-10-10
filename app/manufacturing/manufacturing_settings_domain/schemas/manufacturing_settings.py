"""Pydantic v2 schemas for ManufacturingSettings."""





from __future__ import annotations

from app.manufacturing.manufacturing_settings_domain.models.manufacturing_settings import (

    ManufacturingSettingsBackflushRawMaterialsBasedOn,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ManufacturingSettingsUpdate",

    "ManufacturingSettingsRead",

]





class ManufacturingSettingsUpdate(InputSchema):

    """A partial update of the tenant settings row."""



    material_consumption: Optional[bool] = None

    get_rm_cost_from_consumption_entry: Optional[bool] = None

    backflush_raw_materials_based_on: Optional[ManufacturingSettingsBackflushRawMaterialsBasedOn] = None

    validate_components_quantities_per_bom: Optional[bool] = None

    update_bom_costs_automatically: Optional[bool] = None

    allow_editing_of_items_and_quantities_in_work_order: Optional[bool] = None

    overproduction_percentage_for_sales_order: Optional[Decimal] = None

    overproduction_percentage_for_work_order: Optional[Decimal] = None

    transfer_extra_materials_percentage: Optional[Decimal] = None

    add_corrective_operation_cost_in_finished_good_valuation: Optional[bool] = None

    enforce_time_logs: Optional[bool] = None

    job_card_excess_transfer: Optional[bool] = None

    disable_capacity_planning: Optional[bool] = None

    allow_overtime: Optional[bool] = None

    allow_production_on_holidays: Optional[bool] = None

    capacity_planning_for_days: Optional[int] = None

    mins_between_operations: Optional[int] = None

    set_op_cost_and_secondary_items_from_sub_assemblies: Optional[bool] = None

    make_serial_no_batch_from_work_order: Optional[bool] = None





class ManufacturingSettingsRead(ReadSchema):

    id: uuid.UUID

    material_consumption: Optional[bool] = None

    get_rm_cost_from_consumption_entry: Optional[bool] = None

    backflush_raw_materials_based_on: Optional[ManufacturingSettingsBackflushRawMaterialsBasedOn] = None

    validate_components_quantities_per_bom: Optional[bool] = None

    update_bom_costs_automatically: Optional[bool] = None

    allow_editing_of_items_and_quantities_in_work_order: Optional[bool] = None

    overproduction_percentage_for_sales_order: Optional[Decimal] = None

    overproduction_percentage_for_work_order: Optional[Decimal] = None

    transfer_extra_materials_percentage: Optional[Decimal] = None

    add_corrective_operation_cost_in_finished_good_valuation: Optional[bool] = None

    enforce_time_logs: Optional[bool] = None

    job_card_excess_transfer: Optional[bool] = None

    disable_capacity_planning: Optional[bool] = None

    allow_overtime: Optional[bool] = None

    allow_production_on_holidays: Optional[bool] = None

    capacity_planning_for_days: Optional[int] = None

    mins_between_operations: Optional[int] = None

    set_op_cost_and_secondary_items_from_sub_assemblies: Optional[bool] = None

    make_serial_no_batch_from_work_order: Optional[bool] = None



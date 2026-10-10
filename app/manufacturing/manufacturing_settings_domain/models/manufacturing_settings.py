"""

Manufacturing Settings -- converted from ``erpnext/manufacturing/doctype/manufacturing_settings``.



A Frappe Single (``issingle: 1``): one row per ``business_id``, enforced by a unique constraint on ``business_id`` alone.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, Integer, Numeric, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["ManufacturingSettings", "ManufacturingSettingsBackflushRawMaterialsBasedOn"]





class ManufacturingSettingsBackflushRawMaterialsBasedOn(str, enum.Enum):

    BOM = "BOM"

    MATERIAL_TRANSFERRED_FOR_MANUFACTURE = "Material Transferred for Manufacture"





class ManufacturingSettings(TenantModel):

    __tablename__ = "manufacturing_settingss"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_manufacturing_settingss_business"),

    )



    material_consumption: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    get_rm_cost_from_consumption_entry: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    backflush_raw_materials_based_on: Mapped[Optional[str]] = mapped_column(SAEnum(ManufacturingSettingsBackflushRawMaterialsBasedOn, native_enum=False, length=40, validate_strings=True), nullable=True)

    validate_components_quantities_per_bom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    update_bom_costs_automatically: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_editing_of_items_and_quantities_in_work_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    overproduction_percentage_for_sales_order: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    overproduction_percentage_for_work_order: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    transfer_extra_materials_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    add_corrective_operation_cost_in_finished_good_valuation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    enforce_time_logs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    job_card_excess_transfer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    disable_capacity_planning: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_overtime: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_production_on_holidays: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    capacity_planning_for_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=30)

    mins_between_operations: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    set_op_cost_and_secondary_items_from_sub_assemblies: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    make_serial_no_batch_from_work_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ManufacturingSettings id={self.id}>"

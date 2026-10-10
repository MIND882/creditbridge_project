"""

Work Order -- converted from ``erpnext/manufacturing/doctype/work_order``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, DateTime, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.work_order_operation_domain.models.work_order_operation import WorkOrderOperation

from app.manufacturing.work_order_item_domain.models.work_order_item import WorkOrderItem

from app.manufacturing.work_order_additional_item_domain.models.work_order_additional_item import WorkOrderAdditionalItem

from app.manufacturing.work_order_additional_item_domain.models.work_order_additional_item import WorkOrderAdditionalItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["WorkOrder", "WorkOrderNamingSeries", "WorkOrderTransferMaterialAgainst", "WorkOrderStatus"]





class WorkOrderNamingSeries(str, enum.Enum):

    MFG_WO_YYYY = "MFG-WO-.YYYY.-"



class WorkOrderTransferMaterialAgainst(str, enum.Enum):

    WORK_ORDER = "Work Order"

    JOB_CARD = "Job Card"



class WorkOrderStatus(str, enum.Enum):

    DRAFT = "Draft"

    SUBMITTED = "Submitted"

    NOT_STARTED = "Not Started"

    IN_PROCESS = "In Process"

    STOCK_RESERVED = "Stock Reserved"

    STOCK_PARTIALLY_RESERVED = "Stock Partially Reserved"

    COMPLETED = "Completed"

    STOPPED = "Stopped"

    CLOSED = "Closed"

    CANCELLED = "Cancelled"





class WorkOrder(SubmittableModel, TenantModel):

    __tablename__ = "work_orders"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_work_orders_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    company: Mapped[str] = mapped_column(String(140), nullable=False)

    naming_series: Mapped[str] = mapped_column(SAEnum(WorkOrderNamingSeries, native_enum=False, length=18, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    production_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    production_item = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[production_item_id])

    bom_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    bom_no = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[bom_no_id])

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=1.0)

    sales_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    sales_order = relationship("app.selling.sales_order_domain.models.sales_order.SalesOrder", foreign_keys=[sales_order_id])

    reserve_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    max_producible_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    material_transferred_for_manufacturing: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    additional_transferred_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    produced_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    process_loss_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    disassembled_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    source_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    source_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[source_warehouse_id])

    wip_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    wip_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[wip_warehouse_id])

    fg_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    fg_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[fg_warehouse_id])

    scrap_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    scrap_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[scrap_warehouse_id])

    transfer_material_against: Mapped[Optional[str]] = mapped_column(SAEnum(WorkOrderTransferMaterialAgainst, native_enum=False, length=14, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    allow_alternative_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    use_multi_level_bom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    skip_transfer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    from_wip_warehouse: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    update_consumed_material_cost_in_project: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    planned_start_date: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False)

    planned_end_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    expected_delivery_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    actual_start_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    actual_end_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    lead_time: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    planned_operating_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    actual_operating_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    additional_operating_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    corrective_operation_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_operating_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    has_serial_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    has_batch_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    batch_size: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    subcontracting_inward_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    production_plan_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("production_plans.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    production_plan = relationship("app.manufacturing.production_plan_domain.models.production_plan.ProductionPlan", foreign_keys=[production_plan_id])

    mps_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("master_production_schedules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    mps = relationship("app.manufacturing.master_production_schedule_domain.models.master_production_schedule.MasterProductionSchedule", foreign_keys=[mps_id])

    material_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    material_request = relationship("app.stock.material_request_domain.models.material_request.MaterialRequest", foreign_keys=[material_request_id])

    material_request_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    subcontracting_inward_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    production_plan_sub_assembly_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    production_plan_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    product_bundle_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    product_bundle_item = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[product_bundle_item_id])

    status: Mapped[str] = mapped_column(SAEnum(WorkOrderStatus, native_enum=False, length=28, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    track_semi_finished_goods: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("work_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.manufacturing.work_order_domain.models.work_order.WorkOrder", foreign_keys=[amended_from_id])



    operations: Mapped[list["WorkOrderOperation"]] = relationship(  # noqa: F821

        "app.manufacturing.work_order_operation_domain.models.work_order_operation.WorkOrderOperation",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[WorkOrderOperation.parent_id],

    )



    required_items: Mapped[list["WorkOrderItem"]] = relationship(  # noqa: F821

        "app.manufacturing.work_order_item_domain.models.work_order_item.WorkOrderItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[WorkOrderItem.parent_id],

    )



    non_stock_items: Mapped[list["WorkOrderAdditionalItem"]] = relationship(  # noqa: F821

        "app.manufacturing.work_order_additional_item_domain.models.work_order_additional_item.WorkOrderAdditionalItem",

        primaryjoin="and_(WorkOrder.id == WorkOrderAdditionalItem.parent_id, WorkOrderAdditionalItem.parentfield == 'non_stock_items')",

        overlaps="secondary_items",

        # shared child doctype: rows are separated by parentfield

        cascade="all, delete-orphan",

        foreign_keys=[WorkOrderAdditionalItem.parent_id],

    )



    secondary_items: Mapped[list["WorkOrderAdditionalItem"]] = relationship(  # noqa: F821

        "app.manufacturing.work_order_additional_item_domain.models.work_order_additional_item.WorkOrderAdditionalItem",

        primaryjoin="and_(WorkOrder.id == WorkOrderAdditionalItem.parent_id, WorkOrderAdditionalItem.parentfield == 'secondary_items')",

        overlaps="non_stock_items",

        # shared child doctype: rows are separated by parentfield

        cascade="all, delete-orphan",

        foreign_keys=[WorkOrderAdditionalItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<WorkOrder id={self.id}>"

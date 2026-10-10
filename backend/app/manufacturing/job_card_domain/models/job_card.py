"""

Job Card -- converted from ``erpnext/manufacturing/doctype/job_card``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.job_card_item_domain.models.job_card_item import JobCardItem

from app.manufacturing.job_card_scheduled_time_domain.models.job_card_scheduled_time import JobCardScheduledTime

from app.manufacturing.job_card_time_log_domain.models.job_card_time_log import JobCardTimeLog

from app.manufacturing.job_card_operation_domain.models.job_card_operation import JobCardOperation

from app.manufacturing.job_card_secondary_item_domain.models.job_card_secondary_item import JobCardSecondaryItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["JobCard", "JobCardNamingSeries", "JobCardStatus"]





class JobCardNamingSeries(str, enum.Enum):

    PO_JOB = "PO-JOB.#####"



class JobCardStatus(str, enum.Enum):

    OPEN = "Open"

    WORK_IN_PROGRESS = "Work In Progress"

    PARTIALLY_TRANSFERRED = "Partially Transferred"

    MATERIAL_TRANSFERRED = "Material Transferred"

    ON_HOLD = "On Hold"

    SUBMITTED = "Submitted"

    TO_MANUFACTURE = "To Manufacture"

    CANCELLED = "Cancelled"

    COMPLETED = "Completed"





class JobCard(SubmittableModel, TenantModel):

    __tablename__ = "job_cards"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_job_cards_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    work_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("work_orders.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    work_order = relationship("app.manufacturing.work_order_domain.models.work_order.WorkOrder", foreign_keys=[work_order_id])

    production_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    production_item = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[production_item_id])

    bom_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bom_no = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[bom_no_id])

    for_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    naming_series: Mapped[str] = mapped_column(SAEnum(JobCardNamingSeries, native_enum=False, length=16, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    finished_good_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    finished_good = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[finished_good_id])

    semi_fg_bom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    semi_fg_bom = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[semi_fg_bom_id])

    pending_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    process_loss_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_completed_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    transferred_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    manufactured_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    operation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("operations.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    operation = relationship("app.manufacturing.operation_domain.models.operation.Operation", foreign_keys=[operation_id])

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

    skip_material_transfer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    backflush_from_wip_warehouse: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    workstation_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstation_types.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    workstation_type = relationship("app.manufacturing.workstation_type_domain.models.workstation_type.WorkstationType", foreign_keys=[workstation_type_id])

    workstation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstations.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    workstation = relationship("app.manufacturing.workstation_domain.models.workstation.Workstation", foreign_keys=[workstation_id])

    target_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    target_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[target_warehouse_id])

    quality_inspection_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspection_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    quality_inspection_template = relationship("app.stock.quality_inspection_template_domain.models.quality_inspection_template.QualityInspectionTemplate", foreign_keys=[quality_inspection_template_id])

    quality_inspection_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspections.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    quality_inspection = relationship("app.stock.quality_inspection_domain.models.quality_inspection.QualityInspection", foreign_keys=[quality_inspection_id])

    expected_start_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    time_required: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    expected_end_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    actual_start_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    total_time_in_mins: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    actual_end_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    for_job_card_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("job_cards.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    for_job_card = relationship("app.manufacturing.job_card_domain.models.job_card.JobCard", foreign_keys=[for_job_card_id])

    is_corrective_job_card: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    hour_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    for_operation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("operations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    for_operation = relationship("app.manufacturing.operation_domain.models.operation.Operation", foreign_keys=[for_operation_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    requested_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    is_paused: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_subcontracted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    track_semi_finished_goods: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(JobCardStatus, native_enum=False, length=25, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    operation_row_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("job_cards.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.manufacturing.job_card_domain.models.job_card.JobCard", foreign_keys=[amended_from_id])

    sequence_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    serial_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    serial_and_batch_bundle = relationship("app.stock.serial_and_batch_bundle_domain.models.serial_and_batch_bundle.SerialAndBatchBundle", foreign_keys=[serial_and_batch_bundle_id])

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batches.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("app.stock.batch_domain.models.batch.Batch", foreign_keys=[batch_no_id])



    items: Mapped[list["JobCardItem"]] = relationship(  # noqa: F821

        "app.manufacturing.job_card_item_domain.models.job_card_item.JobCardItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[JobCardItem.parent_id],

    )



    scheduled_time_logs: Mapped[list["JobCardScheduledTime"]] = relationship(  # noqa: F821

        "app.manufacturing.job_card_scheduled_time_domain.models.job_card_scheduled_time.JobCardScheduledTime",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[JobCardScheduledTime.parent_id],

    )



    time_logs: Mapped[list["JobCardTimeLog"]] = relationship(  # noqa: F821

        "app.manufacturing.job_card_time_log_domain.models.job_card_time_log.JobCardTimeLog",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[JobCardTimeLog.parent_id],

    )



    sub_operations: Mapped[list["JobCardOperation"]] = relationship(  # noqa: F821

        "app.manufacturing.job_card_operation_domain.models.job_card_operation.JobCardOperation",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[JobCardOperation.parent_id],

    )



    secondary_items: Mapped[list["JobCardSecondaryItem"]] = relationship(  # noqa: F821

        "app.manufacturing.job_card_secondary_item_domain.models.job_card_secondary_item.JobCardSecondaryItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[JobCardSecondaryItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<JobCard id={self.id}>"

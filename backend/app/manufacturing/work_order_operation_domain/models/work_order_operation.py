"""

Work Order Operation -- converted from ``erpnext/manufacturing/doctype/work_order_operation``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Work Order).

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["WorkOrderOperation", "WorkOrderOperationStatus"]





class WorkOrderOperationStatus(str, enum.Enum):

    PENDING = "Pending"

    WORK_IN_PROGRESS = "Work in Progress"

    COMPLETED = "Completed"





class WorkOrderOperation(ChildTableModel, TenantModel):

    __tablename__ = "work_order_operations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_work_order_operations_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("work_orders.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.work_order_domain.models.work_order.WorkOrder",

        back_populates="operations",

        # explicit: a child can carry a second FK to its own parent

        # (item_variant_attribute.variant_of -> items), which would

        # otherwise make the join ambiguous

        foreign_keys=[parent_id],

    )

    parenttype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    parentfield: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    operation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("operations.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    operation = relationship("app.manufacturing.operation_domain.models.operation.Operation", foreign_keys=[operation_id])

    status: Mapped[Optional[str]] = mapped_column(SAEnum(WorkOrderOperationStatus, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    completed_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    process_loss_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    pending_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    bom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bom = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[bom_id])

    workstation_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstation_types.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    workstation_type = relationship("app.manufacturing.workstation_type_domain.models.workstation_type.WorkstationType", foreign_keys=[workstation_type_id])

    workstation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    workstation = relationship("app.manufacturing.workstation_domain.models.workstation.Workstation", foreign_keys=[workstation_id])

    sequence_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    quality_inspection_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    bom_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bom_no = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[bom_no_id])

    finished_good_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    finished_good = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[finished_good_id])

    is_subcontracted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    skip_material_transfer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    backflush_from_wip_warehouse: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

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

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    planned_start_time: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    hour_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    time_in_mins: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    planned_end_time: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    batch_size: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=1)

    planned_operating_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    actual_start_time: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    actual_operation_time: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    actual_end_time: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    actual_operating_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<WorkOrderOperation id={self.id}>"

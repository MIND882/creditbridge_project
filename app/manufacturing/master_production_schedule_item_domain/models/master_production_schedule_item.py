"""

Master Production Schedule Item -- converted from ``erpnext/manufacturing/doctype/master_production_schedule_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Master Production Schedule).

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["MasterProductionScheduleItem"]







class MasterProductionScheduleItem(ChildTableModel, TenantModel):

    __tablename__ = "master_production_schedule_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_master_production_schedule_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("master_production_schedules.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.master_production_schedule_domain.models.master_production_schedule.MasterProductionSchedule",

        back_populates="items",

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



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_code_id])

    delivery_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    cumulative_lead_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=1)

    order_release_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    planned_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[warehouse_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bom_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bom_no = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[bom_no_id])

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<MasterProductionScheduleItem id={self.id}>"

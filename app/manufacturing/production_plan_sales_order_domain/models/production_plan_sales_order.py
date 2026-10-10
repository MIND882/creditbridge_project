"""

Production Plan Sales Order -- converted from ``erpnext/manufacturing/doctype/production_plan_sales_order``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Master Production Schedule).

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ProductionPlanSalesOrder"]







class ProductionPlanSalesOrder(ChildTableModel, TenantModel):

    __tablename__ = "production_plan_sales_orders"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_production_plan_sales_orders_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("master_production_schedules.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.master_production_schedule_domain.models.master_production_schedule.MasterProductionSchedule",

        back_populates="sales_orders",

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



    sales_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_orders.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    sales_order = relationship("app.selling.sales_order_domain.models.sales_order.SalesOrder", foreign_keys=[sales_order_id])

    sales_order_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("selling_customers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    customer = relationship("app.selling.customer_domain.models.customer.Customer", foreign_keys=[customer_id])

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    status: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProductionPlanSalesOrder id={self.id}>"

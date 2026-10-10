"""

Production Plan Item Reference -- converted from ``erpnext/manufacturing/doctype/production_plan_item_reference``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Production Plan).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ProductionPlanItemReference"]







class ProductionPlanItemReference(ChildTableModel, TenantModel):

    __tablename__ = "production_plan_item_references"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_production_plan_item_references_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("production_plans.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.production_plan_domain.models.production_plan.ProductionPlan",

        back_populates="prod_plan_references",

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



    item_reference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    sales_order = relationship("app.selling.sales_order_domain.models.sales_order.SalesOrder", foreign_keys=[sales_order_id])

    sales_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProductionPlanItemReference id={self.id}>"

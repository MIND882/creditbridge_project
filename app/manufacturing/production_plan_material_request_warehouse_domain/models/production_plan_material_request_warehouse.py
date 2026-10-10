"""

Production Plan Material Request Warehouse -- converted from ``erpnext/manufacturing/doctype/production_plan_material_request_warehouse``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Production Plan).

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ProductionPlanMaterialRequestWarehouse"]







class ProductionPlanMaterialRequestWarehouse(ChildTableModel, TenantModel):

    __tablename__ = "production_plan_material_request_warehouses"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_production_plan_material_request_warehouses_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("production_plans.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.production_plan_domain.models.production_plan.ProductionPlan",

        back_populates="warehouses",

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



    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[warehouse_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProductionPlanMaterialRequestWarehouse id={self.id}>"

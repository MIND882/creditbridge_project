"""

Production Plan Sub Assembly Item -- converted from ``erpnext/manufacturing/doctype/production_plan_sub_assembly_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Production Plan).

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ProductionPlanSubAssemblyItem", "ProductionPlanSubAssemblyItemTypeOfManufacturing"]





class ProductionPlanSubAssemblyItemTypeOfManufacturing(str, enum.Enum):

    IN_HOUSE = "In House"

    SUBCONTRACT = "Subcontract"

    MATERIAL_REQUEST = "Material Request"





class ProductionPlanSubAssemblyItem(ChildTableModel, TenantModel):

    __tablename__ = "production_plan_sub_assembly_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_production_plan_sub_assembly_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("production_plans.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.production_plan_domain.models.production_plan.ProductionPlan",

        back_populates="sub_assembly_items",

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



    production_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    production_item = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[production_item_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    fg_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    fg_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[fg_warehouse_id])

    parent_item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parent_item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[parent_item_code_id])

    bom_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bom_no = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[bom_no_id])

    bom_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    type_of_manufacturing: Mapped[Optional[str]] = mapped_column(SAEnum(ProductionPlanSubAssemblyItemTypeOfManufacturing, native_enum=False, length=20, validate_strings=True), nullable=True)

    required_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    projected_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    supplier_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("suppliers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    supplier = relationship("app.buying.supplier_domain.models.supplier.Supplier", foreign_keys=[supplier_id])

    purchase_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    purchase_order = relationship("app.buying.purchase_order_domain.models.purchase_order.PurchaseOrder", foreign_keys=[purchase_order_id])

    sales_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    sales_order = relationship("app.selling.sales_order_domain.models.sales_order.SalesOrder", foreign_keys=[sales_order_id])

    sales_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    production_plan_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    wo_produced_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_reserved_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ordered_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    received_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    indent: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    schedule_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProductionPlanSubAssemblyItem id={self.id}>"

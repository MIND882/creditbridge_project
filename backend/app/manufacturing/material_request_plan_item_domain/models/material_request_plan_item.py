"""

Material Request Plan Item -- converted from ``erpnext/manufacturing/doctype/material_request_plan_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Production Plan).

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["MaterialRequestPlanItem", "MaterialRequestPlanItemMaterialRequestType"]





class MaterialRequestPlanItemMaterialRequestType(str, enum.Enum):

    PURCHASE = "Purchase"

    MATERIAL_TRANSFER = "Material Transfer"

    MATERIAL_ISSUE = "Material Issue"

    MANUFACTURE = "Manufacture"

    SUBCONTRACTING = "Subcontracting"

    CUSTOMER_PROVIDED = "Customer Provided"





class MaterialRequestPlanItem(ChildTableModel, TenantModel):

    __tablename__ = "material_request_plan_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_material_request_plan_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("production_plans.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.production_plan_domain.models.production_plan.ProductionPlan",

        back_populates="mr_items",

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

        nullable=False, index=True,

    )

    item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_code_id])

    from_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    from_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[from_warehouse_id])

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[warehouse_id])

    material_request_type: Mapped[Optional[str]] = mapped_column(SAEnum(MaterialRequestPlanItemMaterialRequestType, native_enum=False, length=21, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    conversion_factor: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    from_bom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    from_bom = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[from_bom_id])

    main_item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    main_item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[main_item_code_id])

    required_bom_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    projected_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    quantity: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_reserved_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    schedule_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    min_order_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    sales_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    sales_order = relationship("app.selling.sales_order_domain.models.sales_order.SalesOrder", foreign_keys=[sales_order_id])

    sub_assembly_item_reference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    requested_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    reserved_qty_for_production: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ordered_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    safety_stock: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<MaterialRequestPlanItem id={self.id}>"

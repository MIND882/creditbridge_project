"""

Purchase Order Item -- converted from ``erpnext/buying/doctype/purchase_order_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Purchase Order).

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PurchaseOrderItem", "PurchaseOrderItemMarginType"]





class PurchaseOrderItemMarginType(str, enum.Enum):

    PERCENTAGE = "Percentage"

    AMOUNT = "Amount"





class PurchaseOrderItem(ChildTableModel, TenantModel):

    __tablename__ = "purchase_order_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_purchase_order_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_orders.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "PurchaseOrder",

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

        nullable=False, index=True,

    )

    item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_code_id])

    supplier_part_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_name: Mapped[str] = mapped_column(String(140), nullable=False)

    schedule_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    expected_delivery_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    image_view: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    last_purchase_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    base_amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    pricing_rules: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_free_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    net_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    weight_per_unit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    weight_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    weight_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[weight_uom_id])

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[warehouse_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    material_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    material_request = relationship("app.stock.material_request_domain.models.material_request.MaterialRequest", foreign_keys=[material_request_id])

    material_request_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_quotation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_quotations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    supplier_quotation = relationship("app.buying.supplier_quotation_domain.models.supplier_quotation.SupplierQuotation", foreign_keys=[supplier_quotation_id])

    supplier_quotation_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_quotation_items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    supplier_quotation_item = relationship("app.buying.supplier_quotation_item_domain.models.supplier_quotation_item.SupplierQuotationItem", foreign_keys=[supplier_quotation_item_id])

    delivered_by_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    blanket_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    blanket_order_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("app.stock.item_group_domain.models.item_group.ItemGroup", foreign_keys=[item_group_id])

    brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("brands.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    brand = relationship("app.stock.brand_domain.models.brand.Brand", foreign_keys=[brand_id])

    bom: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    received_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    returned_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    billed_amt: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_tax_rate: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("app.accounts.account_domain.models.account.Account", foreign_keys=[expense_account_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("app.accounts.cost_center_domain.models.cost_center.CostCenter", foreign_keys=[cost_center_id])

    page_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    item_tax_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_tax_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_tax_template = relationship("app.accounts.item_tax_template_domain.models.item_tax_template.ItemTaxTemplate", foreign_keys=[item_tax_template_id])

    manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("manufacturers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    manufacturer = relationship("app.stock.manufacturer_domain.models.manufacturer.Manufacturer", foreign_keys=[manufacturer_id])

    manufacturer_part_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    against_blanket_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_fixed_asset: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    stock_uom_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    company_total_stock: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    margin_type: Mapped[Optional[str]] = mapped_column(SAEnum(PurchaseOrderItemMarginType, native_enum=False, length=14, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    margin_rate_or_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    production_plan: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    production_plan_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    production_plan_sub_assembly_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    product_bundle: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_order_packed_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    fg_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    fg_item = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[fg_item_id])

    fg_item_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=1)

    from_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    from_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[from_warehouse_id])

    wip_composite_asset: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    job_card: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    distributed_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    subcontracted_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PurchaseOrderItem id={self.id}>"

"""

Quotation Item -- converted from ``erpnext/selling/doctype/quotation_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Quotation).

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["QuotationItem", "QuotationItemMarginType"]





class QuotationItemMarginType(str, enum.Enum):

    PERCENTAGE = "Percentage"

    AMOUNT = "Amount"





class QuotationItem(ChildTableModel, TenantModel):

    __tablename__ = "selling_quotation_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_selling_quotation_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("selling_quotations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.selling.quotation_domain.models.quotation.Quotation",

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

    is_product_bundle: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    product_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("product_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    product_bundle = relationship("app.selling.product_bundle_domain.models.product_bundle.ProductBundle", foreign_keys=[product_bundle_id])

    item_name: Mapped[str] = mapped_column(String(140), nullable=False)

    customer_item_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_free_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_alternative: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    has_alternative_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

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

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    image_view: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ordered_qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    company_total_stock: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    margin_type: Mapped[Optional[str]] = mapped_column(SAEnum(QuotationItemMarginType, values_callable=lambda x: [e.value for e in x], native_enum=False, length=14, validate_strings=True), nullable=True)

    margin_rate_or_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    distributed_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_tax_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_tax_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_tax_template = relationship("app.accounts.item_tax_template_domain.models.item_tax_template.ItemTaxTemplate", foreign_keys=[item_tax_template_id])

    base_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    pricing_rules: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    stock_uom_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    valuation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    gross_profit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

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

    against_blanket_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    blanket_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    blanket_order_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    prevdoc_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    prevdoc_docname: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    projected_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_tax_rate: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    additional_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    page_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<QuotationItem id={self.id}>"

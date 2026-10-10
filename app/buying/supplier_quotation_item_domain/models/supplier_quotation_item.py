"""

Supplier Quotation Item -- converted from ``erpnext/buying/doctype/supplier_quotation_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Supplier Quotation).

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SupplierQuotationItem", "SupplierQuotationItemMarginType"]





class SupplierQuotationItemMarginType(str, enum.Enum):

    PERCENTAGE = "Percentage"

    AMOUNT = "Amount"





class SupplierQuotationItem(ChildTableModel, TenantModel):

    __tablename__ = "supplier_quotation_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_supplier_quotation_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_quotations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "SupplierQuotation",

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

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    lead_time_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    image_view: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    base_amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    pricing_rules: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

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

    prevdoc_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    material_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    material_request = relationship("app.stock.material_request_domain.models.material_request.MaterialRequest", foreign_keys=[material_request_id])

    sales_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    request_for_quotation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("request_for_quotations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    request_for_quotation = relationship("app.buying.request_for_quotation_domain.models.request_for_quotation.RequestForQuotation", foreign_keys=[request_for_quotation_id])

    item_tax_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_tax_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_tax_template = relationship("app.accounts.item_tax_template_domain.models.item_tax_template.ItemTaxTemplate", foreign_keys=[item_tax_template_id])

    material_request_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    request_for_quotation_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("brands.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    brand = relationship("app.stock.brand_domain.models.brand.Brand", foreign_keys=[brand_id])

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("app.stock.item_group_domain.models.item_group.ItemGroup", foreign_keys=[item_group_id])

    item_tax_rate: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    page_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("manufacturers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    manufacturer = relationship("app.stock.manufacturer_domain.models.manufacturer.Manufacturer", foreign_keys=[manufacturer_id])

    manufacturer_part_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_free_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    expected_delivery_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("app.accounts.cost_center_domain.models.cost_center.CostCenter", foreign_keys=[cost_center_id])

    distributed_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    margin_type: Mapped[Optional[str]] = mapped_column(SAEnum(SupplierQuotationItemMarginType, native_enum=False, length=14, validate_strings=True), nullable=True)

    margin_rate_or_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierQuotationItem id={self.id}>"

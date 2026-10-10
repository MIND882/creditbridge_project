"""

Purchase Invoice Item -- converted from ``erpnext/accounts/doctype/purchase_invoice_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401

from app.accounts.item_tax_template_domain.models.item_tax_template import ItemTaxTemplate  # noqa: F401

from app.accounts.tax_withholding_category_domain.models.tax_withholding_category import TaxWithholdingCategory  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PurchaseInvoiceItem", "PurchaseInvoiceItemMarginType"]







class PurchaseInvoiceItemMarginType(str, enum.Enum):

    PERCENTAGE = "Percentage"

    AMOUNT = "Amount"









class PurchaseInvoiceItem(ChildTableModel, TenantModel):

    __tablename__ = "purchase_invoice_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_purchase_invoice_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_invoices.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PurchaseInvoice", back_populates="items", foreign_keys=[parent_id])



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    item_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_name: Mapped[str] = mapped_column(String(140), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    image_view: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    received_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    rejected_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    uom: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    base_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    base_amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    pricing_rules: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_free_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    net_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    weight_per_unit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    weight_uom: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    rejected_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    quality_inspection: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    batch_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    rejected_serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("Account", foreign_keys=[expense_account_id])

    item_tax_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_tax_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_tax_template = relationship("ItemTaxTemplate", foreign_keys=[item_tax_template_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    deferred_expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    deferred_expense_account = relationship("Account", foreign_keys=[deferred_expense_account_id])

    service_stop_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    enable_deferred_expense: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    service_start_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    service_end_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    allow_zero_valuation_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    brand: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_tax_rate: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    item_tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    purchase_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    include_exploded_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_fixed_asset: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    asset_location: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    po_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    purchase_receipt: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    page_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    pr_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    valuation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rm_supp_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    landed_cost_voucher_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    manufacturer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    manufacturer_part_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    asset_category: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    from_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    purchase_invoice_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    stock_uom_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    sales_invoice_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    margin_type: Mapped[Optional[PurchaseInvoiceItemMarginType]] = mapped_column(

        SAEnum(PurchaseInvoiceItemMarginType, native_enum=False, length=10, validate_strings=True),

        nullable=True,

    )

    margin_rate_or_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    product_bundle: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    apply_tds: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    serial_and_batch_bundle: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    rejected_serial_and_batch_bundle: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    wip_composite_asset: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    use_serial_batch_fields: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    material_request: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    material_request_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_incoming_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    distributed_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_withholding_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_withholding_category = relationship("TaxWithholdingCategory", foreign_keys=[tax_withholding_category_id])

    delivered_by_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PurchaseInvoiceItem id={self.id}>"

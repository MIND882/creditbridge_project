"""

Sales Invoice Item -- converted from ``erpnext/accounts/doctype/sales_invoice_item``.



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

from app.accounts.finance_book_domain.models.finance_book import FinanceBook  # noqa: F401

from app.accounts.item_tax_template_domain.models.item_tax_template import ItemTaxTemplate  # noqa: F401

from app.accounts.tax_withholding_category_domain.models.tax_withholding_category import TaxWithholdingCategory  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SalesInvoiceItem", "SalesInvoiceItemMarginType"]







class SalesInvoiceItemMarginType(str, enum.Enum):

    PERCENTAGE = "Percentage"

    AMOUNT = "Amount"









class SalesInvoiceItem(ChildTableModel, TenantModel):

    __tablename__ = "sales_invoice_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_sales_invoice_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_invoices.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("SalesInvoice", back_populates="items", foreign_keys=[parent_id])



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_product_bundle: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    product_bundle: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_name: Mapped[str] = mapped_column(String(140), nullable=False)

    customer_item_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image_view: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    uom: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    margin_type: Mapped[Optional[SalesInvoiceItemMarginType]] = mapped_column(

        SAEnum(SalesInvoiceItemMarginType, native_enum=False, length=10, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    margin_rate_or_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

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

    delivered_by_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    income_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    income_account = relationship("Account", foreign_keys=[income_account_id])

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

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    deferred_revenue_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    deferred_revenue_account = relationship("Account", foreign_keys=[deferred_revenue_account_id])

    service_stop_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    enable_deferred_revenue: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    service_start_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    service_end_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    weight_per_unit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    weight_uom: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    target_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    quality_inspection: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    batch_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    allow_zero_valuation_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    item_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    brand: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_tax_rate: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    actual_batch_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    sales_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    so_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivery_note: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dn_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivered_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    is_fixed_asset: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    asset: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    page_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    finance_book_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("finance_books.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    finance_book = relationship("FinanceBook", foreign_keys=[finance_book_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_invoice_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    incoming_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    discount_account = relationship("Account", foreign_keys=[discount_account_id])

    grant_commission: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    purchase_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    purchase_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    has_item_scanned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    serial_and_batch_bundle: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    use_serial_batch_fields: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    distributed_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    company_total_stock: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    pos_invoice_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pos_invoice: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    scio_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_withholding_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_withholding_category = relationship("TaxWithholdingCategory", foreign_keys=[tax_withholding_category_id])

    apply_tds: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    against_pick_list: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pick_list_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SalesInvoiceItem id={self.id}>"

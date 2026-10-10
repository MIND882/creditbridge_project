"""

Quotation -- converted from ``erpnext/selling/doctype/quotation``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.selling.quotation_item_domain.models.quotation_item import QuotationItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["Quotation", "QuotationNamingSeries", "QuotationOrderType", "QuotationApplyDiscountOn", "QuotationStatus"]





class QuotationNamingSeries(str, enum.Enum):

    SAL_QTN_YYYY = "SAL-QTN-.YYYY.-"



class QuotationOrderType(str, enum.Enum):

    SALES = "Sales"

    MAINTENANCE = "Maintenance"

    SHOPPING_CART = "Shopping Cart"



class QuotationApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"



class QuotationStatus(str, enum.Enum):

    DRAFT = "Draft"

    OPEN = "Open"

    REPLIED = "Replied"

    PARTIALLY_ORDERED = "Partially Ordered"

    ORDERED = "Ordered"

    LOST = "Lost"

    CANCELLED = "Cancelled"

    EXPIRED = "Expired"





class Quotation(SubmittableModel, TenantModel):

    __tablename__ = "selling_quotations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_selling_quotations_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(QuotationNamingSeries, values_callable=lambda x: [e.value for e in x], native_enum=False, length=19, validate_strings=True), nullable=False)

    quotation_to: Mapped[str] = mapped_column(String(140), nullable=False)

    party_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    transaction_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    valid_till: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    order_type: Mapped[str] = mapped_column(SAEnum(QuotationOrderType, values_callable=lambda x: [e.value for e in x], native_enum=False, length=17, validate_strings=True), nullable=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    has_unit_price_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("selling_quotations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.selling.quotation_domain.models.quotation.Quotation", foreign_keys=[amended_from_id])

    currency: Mapped[str] = mapped_column(String(140), nullable=False)

    conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    selling_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    selling_price_list = relationship("app.stock.price_list_domain.models.price_list.PriceList", foreign_keys=[selling_price_list_id])

    price_list_currency: Mapped[str] = mapped_column(String(140), nullable=False)

    plc_conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_net_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("app.accounts.tax_category_domain.models.tax_category.TaxCategory", foreign_keys=[tax_category_id])

    taxes_and_charges_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_taxes_and_charges_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    taxes_and_charges = relationship("app.accounts.sales_taxes_and_charges_template_domain.models.sales_taxes_and_charges_template.SalesTaxesAndChargesTemplate", foreign_keys=[taxes_and_charges_id])

    shipping_rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipping_rules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    shipping_rule = relationship("app.accounts.shipping_rule_domain.models.shipping_rule.ShippingRule", foreign_keys=[shipping_rule_id])

    incoterm: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    named_place: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    base_total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    disable_rounded_total: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    base_grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    base_rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    apply_discount_on: Mapped[Optional[str]] = mapped_column(SAEnum(QuotationApplyDiscountOn,values_callable=lambda x: [e.value for e in x],  native_enum=False, length=15, validate_strings=True), nullable=True)

    base_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    coupon_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("coupon_codes.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    coupon_code = relationship("app.accounts.coupon_code_domain.models.coupon_code.CouponCode", foreign_keys=[coupon_code_id])

    additional_discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    referral_sales_partner: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    other_charges_calculation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    customer_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_display: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_mobile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    company_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    company_contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_terms_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    payment_terms_template = relationship("app.accounts.payment_terms_template_domain.models.payment_terms_template.PaymentTermsTemplate", foreign_keys=[payment_terms_template_id])

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    auto_repeat: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    group_same_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    order_lost_reason: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_source: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_medium: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_campaign: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_content: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[str] = mapped_column(SAEnum(QuotationStatus, values_callable=lambda x: [e.value for e in x], native_enum=False, length=21, validate_strings=True), nullable=False)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    territory: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    opportunity: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    enq_det: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    supplier_quotation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_quotations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    supplier_quotation = relationship("app.buying.supplier_quotation_domain.models.supplier_quotation.SupplierQuotation", foreign_keys=[supplier_quotation_id])



    items: Mapped[list["QuotationItem"]] = relationship(  # noqa: F821

        "app.selling.quotation_item_domain.models.quotation_item.QuotationItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys=[QuotationItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Quotation id={self.id}>"

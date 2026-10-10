"""

Supplier Quotation -- converted from ``erpnext/buying/doctype/supplier_quotation``.



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



from app.buying.supplier_quotation_item_domain.models.supplier_quotation_item import SupplierQuotationItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["SupplierQuotation", "SupplierQuotationNamingSeries", "SupplierQuotationApplyDiscountOn", "SupplierQuotationStatus"]





class SupplierQuotationNamingSeries(str, enum.Enum):

    PUR_SQTN_YYYY = "PUR-SQTN-.YYYY.-"



class SupplierQuotationApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"



class SupplierQuotationStatus(str, enum.Enum):

    DRAFT = "Draft"

    SUBMITTED = "Submitted"

    STOPPED = "Stopped"

    CANCELLED = "Cancelled"

    EXPIRED = "Expired"





class SupplierQuotation(SubmittableModel, TenantModel):

    __tablename__ = "supplier_quotations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_supplier_quotations_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    naming_series: Mapped[str] = mapped_column(SAEnum(SupplierQuotationNamingSeries, native_enum=False, length=20, validate_strings=True), nullable=False)

    supplier_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("suppliers.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    supplier = relationship("app.buying.supplier_domain.models.supplier.Supplier", foreign_keys=[supplier_id])

    supplier_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    transaction_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_quotations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.buying.supplier_quotation_domain.models.supplier_quotation.SupplierQuotation", foreign_keys=[amended_from_id])

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    supplier_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contact_display: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_mobile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    currency: Mapped[str] = mapped_column(String(140), nullable=False)

    conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    buying_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    buying_price_list = relationship("app.stock.price_list_domain.models.price_list.PriceList", foreign_keys=[buying_price_list_id])

    price_list_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    plc_conversion_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    total_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_net_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("app.accounts.tax_category_domain.models.tax_category.TaxCategory", foreign_keys=[tax_category_id])

    shipping_rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipping_rules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    shipping_rule = relationship("app.accounts.shipping_rule_domain.models.shipping_rule.ShippingRule", foreign_keys=[shipping_rule_id])

    taxes_and_charges_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_taxes_and_charges_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    taxes_and_charges = relationship("app.accounts.purchase_taxes_and_charges_template_domain.models.purchase_taxes_and_charges_template.PurchaseTaxesAndChargesTemplate", foreign_keys=[taxes_and_charges_id])

    other_charges_calculation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    base_taxes_and_charges_added: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_taxes_and_charges_deducted: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxes_and_charges_added: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxes_and_charges_deducted: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    apply_discount_on: Mapped[Optional[str]] = mapped_column(SAEnum(SupplierQuotationApplyDiscountOn, native_enum=False, length=15, validate_strings=True), nullable=True)

    base_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    additional_discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    base_rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    disable_rounded_total: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    group_same_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    auto_repeat: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[str] = mapped_column(SAEnum(SupplierQuotationStatus, native_enum=False, length=13, validate_strings=True), nullable=False)

    is_subcontracted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    opportunity: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    valid_till: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    quotation_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    incoterm: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    named_place: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    billing_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("app.accounts.cost_center_domain.models.cost_center.CostCenter", foreign_keys=[cost_center_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    has_unit_price_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    items: Mapped[list["SupplierQuotationItem"]] = relationship(  # noqa: F821

        "SupplierQuotationItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[SupplierQuotationItem.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierQuotation id={self.id}>"

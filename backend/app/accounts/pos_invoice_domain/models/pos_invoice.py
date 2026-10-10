"""

POS Invoice -- converted from ``erpnext/accounts/doctype/pos_invoice``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.pos_invoice_item_domain.models.pos_invoice_item import POSInvoiceItem

from app.accounts.pricing_rule_detail_domain.models.pricing_rule_detail import PricingRuleDetail

from app.accounts.sales_invoice_advance_domain.models.sales_invoice_advance import SalesInvoiceAdvance

from app.accounts.sales_invoice_payment_domain.models.sales_invoice_payment import SalesInvoicePayment

from app.accounts.sales_invoice_timesheet_domain.models.sales_invoice_timesheet import SalesInvoiceTimesheet



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401

from app.accounts.payment_terms_template_domain.models.payment_terms_template import PaymentTermsTemplate  # noqa: F401

from app.accounts.tax_category_domain.models.tax_category import TaxCategory  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["POSInvoice", "POSInvoiceNamingSeries", "POSInvoiceApplyDiscountOn", "POSInvoiceStatus", "POSInvoiceIsOpening"]







class POSInvoiceNamingSeries(str, enum.Enum):

    ACC_PSINV_YYYY = "ACC-PSINV-.YYYY.-"





class POSInvoiceApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"





class POSInvoiceStatus(str, enum.Enum):

    DRAFT = "Draft"

    RETURN = "Return"

    CREDIT_NOTE_ISSUED = "Credit Note Issued"

    CONSOLIDATED = "Consolidated"

    SUBMITTED = "Submitted"

    PAID = "Paid"

    PARTLY_PAID = "Partly Paid"

    UNPAID = "Unpaid"

    PARTLY_PAID_AND_DISCOUNTED = "Partly Paid and Discounted"

    UNPAID_AND_DISCOUNTED = "Unpaid and Discounted"

    OVERDUE_AND_DISCOUNTED = "Overdue and Discounted"

    OVERDUE = "Overdue"

    CANCELLED = "Cancelled"





class POSInvoiceIsOpening(str, enum.Enum):

    NO = "No"

    YES = "Yes"









class POSInvoice(SubmittableModel, TenantModel):

    __tablename__ = "pos_invoices"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_pos_invoices_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[POSInvoiceNamingSeries] = mapped_column(

        SAEnum(POSInvoiceNamingSeries, native_enum=False, length=17, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    pos_profile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_return: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    posting_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    set_posting_time: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    due_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    return_against: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    update_billed_amount_in_sales_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    po_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    po_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    customer_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_display: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_mobile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    territory: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    company_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    selling_price_list: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    price_list_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    plc_conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    set_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    update_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_billing_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_total: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_net_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxes_and_charges: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_rule: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("TaxCategory", foreign_keys=[tax_category_id])

    other_charges_calculation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    base_total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    loyalty_points: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    loyalty_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    redeem_loyalty_points: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    loyalty_program: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    loyalty_redemption_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    loyalty_redemption_account = relationship("Account", foreign_keys=[loyalty_redemption_account_id])

    loyalty_redemption_cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    loyalty_redemption_cost_center = relationship("CostCenter", foreign_keys=[loyalty_redemption_cost_center_id])

    apply_discount_on: Mapped[Optional[POSInvoiceApplyDiscountOn]] = mapped_column(

        SAEnum(POSInvoiceApplyDiscountOn, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    base_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    additional_discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_grand_total: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    base_rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    grand_total: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_advance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    outstanding_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    allocate_advances_automatically: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    payment_terms_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    payment_terms_template = relationship("PaymentTermsTemplate", foreign_keys=[payment_terms_template_id])

    cash_bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cash_bank_account = relationship("Account", foreign_keys=[cash_bank_account_id])

    base_paid_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    paid_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_change_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    change_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    account_for_change_amount_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    account_for_change_amount = relationship("Account", foreign_keys=[account_for_change_amount_id])

    write_off_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_write_off_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    write_off_outstanding_amount_automatically: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    write_off_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    write_off_account = relationship("Account", foreign_keys=[write_off_account_id])

    write_off_cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    write_off_cost_center = relationship("CostCenter", foreign_keys=[write_off_cost_center_id])

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    group_same_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    inter_company_invoice_reference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_discounted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    status: Mapped[Optional[POSInvoiceStatus]] = mapped_column(

        SAEnum(POSInvoiceStatus, native_enum=False, length=26, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    debit_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    debit_to = relationship("Account", foreign_keys=[debit_to_id])

    party_account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_opening: Mapped[Optional[POSInvoiceIsOpening]] = mapped_column(

        SAEnum(POSInvoiceIsOpening, native_enum=False, length=3, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    remarks: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_partner: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    commission_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_commission: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    from_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    auto_repeat: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    against_income_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    consolidated_invoice: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    coupon_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amount_eligible_for_commission: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    update_billed_amount_in_delivery_note: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    utm_medium: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_campaign: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_source: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company_contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    items = relationship(

        POSInvoiceItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=POSInvoiceItem.idx,

        passive_deletes=True,

    )

    pricing_rules = relationship(

        PricingRuleDetail,

        primaryjoin="and_(POSInvoice.id == foreign(PricingRuleDetail.parent_id), PricingRuleDetail.parenttype == 'POS Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=PricingRuleDetail.idx,

        overlaps="pricing_rules",

    )

    timesheets = relationship(

        SalesInvoiceTimesheet,

        primaryjoin="and_(POSInvoice.id == foreign(SalesInvoiceTimesheet.parent_id), SalesInvoiceTimesheet.parenttype == 'POS Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=SalesInvoiceTimesheet.idx,

        overlaps="timesheets",

    )

    advances = relationship(

        SalesInvoiceAdvance,

        primaryjoin="and_(POSInvoice.id == foreign(SalesInvoiceAdvance.parent_id), SalesInvoiceAdvance.parenttype == 'POS Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=SalesInvoiceAdvance.idx,

        overlaps="advances",

    )

    payments = relationship(

        SalesInvoicePayment,

        primaryjoin="and_(POSInvoice.id == foreign(SalesInvoicePayment.parent_id), SalesInvoicePayment.parenttype == 'POS Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=SalesInvoicePayment.idx,

        overlaps="payments",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSInvoice id={self.id}>"

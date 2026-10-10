"""

Sales Invoice -- converted from ``erpnext/accounts/doctype/sales_invoice``.



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



from app.accounts.pricing_rule_detail_domain.models.pricing_rule_detail import PricingRuleDetail

from app.accounts.sales_invoice_advance_domain.models.sales_invoice_advance import SalesInvoiceAdvance

from app.accounts.sales_invoice_item_domain.models.sales_invoice_item import SalesInvoiceItem

from app.accounts.sales_invoice_payment_domain.models.sales_invoice_payment import SalesInvoicePayment

from app.accounts.sales_invoice_timesheet_domain.models.sales_invoice_timesheet import SalesInvoiceTimesheet

from app.accounts.tax_withholding_entry_domain.models.tax_withholding_entry import TaxWithholdingEntry



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401

from app.accounts.payment_terms_template_domain.models.payment_terms_template import PaymentTermsTemplate  # noqa: F401

from app.accounts.tax_category_domain.models.tax_category import TaxCategory  # noqa: F401

from app.accounts.tax_withholding_group_domain.models.tax_withholding_group import TaxWithholdingGroup  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["SalesInvoice", "SalesInvoiceNamingSeries", "SalesInvoiceApplyDiscountOn", "SalesInvoiceStatus", "SalesInvoiceIsOpening"]



def _enum_values(e):
    return [m.value for m in e]



class SalesInvoiceNamingSeries(str, enum.Enum):

    ACC_SINV_YYYY = "ACC-SINV-.YYYY.-"

    ACC_SINV_RET_YYYY = "ACC-SINV-RET-.YYYY.-"





class SalesInvoiceApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"





class SalesInvoiceStatus(str, enum.Enum):

    DRAFT = "Draft"

    RETURN = "Return"

    CREDIT_NOTE_ISSUED = "Credit Note Issued"

    SUBMITTED = "Submitted"

    PAID = "Paid"

    PARTLY_PAID = "Partly Paid"

    UNPAID = "Unpaid"

    UNPAID_AND_DISCOUNTED = "Unpaid and Discounted"

    PARTLY_PAID_AND_DISCOUNTED = "Partly Paid and Discounted"

    OVERDUE_AND_DISCOUNTED = "Overdue and Discounted"

    OVERDUE = "Overdue"

    CANCELLED = "Cancelled"

    INTERNAL_TRANSFER = "Internal Transfer"





class SalesInvoiceIsOpening(str, enum.Enum):

    NO = "No"

    YES = "Yes"









class SalesInvoice(SubmittableModel, TenantModel):

    __tablename__ = "sales_invoices"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_sales_invoices_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[SalesInvoiceNamingSeries] = mapped_column(
        SAEnum(SalesInvoiceNamingSeries, native_enum=False, length=20,
            validate_strings=True, values_callable=_enum_values),
        nullable=False,
    )

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    pos_profile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_return: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    posting_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    set_posting_time: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    due_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    return_against: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    update_billed_amount_in_sales_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

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

    apply_discount_on: Mapped[Optional[SalesInvoiceApplyDiscountOn]] = mapped_column(
    SAEnum(SalesInvoiceApplyDiscountOn, native_enum=False, length=11,
           validate_strings=True, values_callable=_enum_values),
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

    status: Mapped[Optional[SalesInvoiceStatus]] = mapped_column(
    SAEnum(SalesInvoiceStatus, native_enum=False, length=26,
           validate_strings=True, values_callable=_enum_values),
    nullable=True,
    )


    debit_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    debit_to = relationship("Account", foreign_keys=[debit_to_id])

    party_account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_opening: Mapped[Optional[SalesInvoiceIsOpening]] = mapped_column(
    SAEnum(SalesInvoiceIsOpening, native_enum=False, length=3,
           validate_strings=True, values_callable=_enum_values),
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

    is_consolidated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_internal_customer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    company_tax_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    unrealized_profit_loss_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    unrealized_profit_loss_account = relationship("Account", foreign_keys=[unrealized_profit_loss_account_id])

    set_target_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_debit_note: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    disable_rounded_total: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    additional_discount_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    additional_discount_account = relationship("Account", foreign_keys=[additional_discount_account_id])

    dispatch_address_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dispatch_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    ignore_default_payment_terms_template: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    total_billing_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount_eligible_for_commission: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    subscription: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_cash_or_non_trade_discount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    incoterm: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    named_place: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    only_include_allocated_payments: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    use_company_roundoff_cost_center: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    update_billed_amount_in_delivery_note: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    dont_create_loyalty_points: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    coupon_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    update_outstanding_for_self: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    utm_medium: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_content: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_campaign: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_source: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company_contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_created_using_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    pos_closing_entry: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    has_subcontracted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    apply_tds: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    tax_withholding_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_withholding_group = relationship("TaxWithholdingGroup", foreign_keys=[tax_withholding_group_id])

    ignore_tax_withholding_threshold: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    override_tax_withholding_entries: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    items = relationship(

        SalesInvoiceItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=SalesInvoiceItem.idx,

        passive_deletes=True,

    )

    pricing_rules = relationship(

        PricingRuleDetail,

        primaryjoin="and_(SalesInvoice.id == foreign(PricingRuleDetail.parent_id), PricingRuleDetail.parenttype == 'Sales Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=PricingRuleDetail.idx,

        overlaps="pricing_rules",

    )

    timesheets = relationship(

        SalesInvoiceTimesheet,

        primaryjoin="and_(SalesInvoice.id == foreign(SalesInvoiceTimesheet.parent_id), SalesInvoiceTimesheet.parenttype == 'Sales Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=SalesInvoiceTimesheet.idx,

        overlaps="timesheets",

    )

    advances = relationship(

        SalesInvoiceAdvance,

        primaryjoin="and_(SalesInvoice.id == foreign(SalesInvoiceAdvance.parent_id), SalesInvoiceAdvance.parenttype == 'Sales Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=SalesInvoiceAdvance.idx,

        overlaps="advances",

    )

    payments = relationship(

        SalesInvoicePayment,

        primaryjoin="and_(SalesInvoice.id == foreign(SalesInvoicePayment.parent_id), SalesInvoicePayment.parenttype == 'Sales Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=SalesInvoicePayment.idx,

        overlaps="payments",

    )

    tax_withholding_entries = relationship(

        TaxWithholdingEntry,

        primaryjoin="and_(SalesInvoice.id == foreign(TaxWithholdingEntry.parent_id), TaxWithholdingEntry.parenttype == 'Sales Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=TaxWithholdingEntry.idx,

        overlaps="tax_withholding_entries",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SalesInvoice id={self.id}>"

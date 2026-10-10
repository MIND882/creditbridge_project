"""

Purchase Invoice -- converted from ``erpnext/accounts/doctype/purchase_invoice``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.pricing_rule_detail_domain.models.pricing_rule_detail import PricingRuleDetail

from app.accounts.purchase_invoice_advance_domain.models.purchase_invoice_advance import PurchaseInvoiceAdvance

from app.accounts.purchase_invoice_item_domain.models.purchase_invoice_item import PurchaseInvoiceItem

from app.accounts.tax_withholding_entry_domain.models.tax_withholding_entry import TaxWithholdingEntry



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401

from app.accounts.mode_of_payment_domain.models.mode_of_payment import ModeOfPayment  # noqa: F401

from app.accounts.payment_terms_template_domain.models.payment_terms_template import PaymentTermsTemplate  # noqa: F401

from app.accounts.tax_category_domain.models.tax_category import TaxCategory  # noqa: F401

from app.accounts.tax_withholding_group_domain.models.tax_withholding_group import TaxWithholdingGroup  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["PurchaseInvoice", "PurchaseInvoiceNamingSeries", "PurchaseInvoiceApplyDiscountOn", "PurchaseInvoiceIsOpening", "PurchaseInvoiceStatus"]







class PurchaseInvoiceNamingSeries(str, enum.Enum):

    ACC_PINV_YYYY = "ACC-PINV-.YYYY.-"

    ACC_PINV_RET_YYYY = "ACC-PINV-RET-.YYYY.-"





class PurchaseInvoiceApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"





class PurchaseInvoiceIsOpening(str, enum.Enum):

    NO = "No"

    YES = "Yes"





class PurchaseInvoiceStatus(str, enum.Enum):

    DRAFT = "Draft"

    RETURN = "Return"

    DEBIT_NOTE_ISSUED = "Debit Note Issued"

    SUBMITTED = "Submitted"

    PAID = "Paid"

    PARTLY_PAID = "Partly Paid"

    UNPAID = "Unpaid"

    OVERDUE = "Overdue"

    CANCELLED = "Cancelled"

    INTERNAL_TRANSFER = "Internal Transfer"









class PurchaseInvoice(SubmittableModel, TenantModel):

    __tablename__ = "purchase_invoices"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_purchase_invoices_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    naming_series: Mapped[PurchaseInvoiceNamingSeries] = mapped_column(

        SAEnum(PurchaseInvoiceNamingSeries, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    supplier_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    due_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    is_paid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_return: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    apply_tds: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    posting_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    set_posting_time: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    on_hold: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    release_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    hold_comment: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bill_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bill_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    return_against: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    update_billed_amount_in_purchase_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    update_billed_amount_in_purchase_receipt: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    supplier_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_display: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_mobile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    conversion_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    buying_price_list: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    price_list_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    plc_conversion_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    set_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    rejected_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_subcontracted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    update_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

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

    tax_category = relationship("TaxCategory", foreign_keys=[tax_category_id])

    shipping_rule: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    taxes_and_charges: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    other_charges_calculation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    base_taxes_and_charges_added: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_taxes_and_charges_deducted: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxes_and_charges_added: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxes_and_charges_deducted: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    apply_discount_on: Mapped[Optional[PurchaseInvoiceApplyDiscountOn]] = mapped_column(

        SAEnum(PurchaseInvoiceApplyDiscountOn, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    base_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    additional_discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_advance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    outstanding_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    disable_rounded_total: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    mode_of_payment_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("mode_of_payments.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    mode_of_payment = relationship("ModeOfPayment", foreign_keys=[mode_of_payment_id])

    cash_bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cash_bank_account = relationship("Account", foreign_keys=[cash_bank_account_id])

    clearance_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    paid_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_paid_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    write_off_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_write_off_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

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

    allocate_advances_automatically: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    payment_terms_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    payment_terms_template = relationship("PaymentTermsTemplate", foreign_keys=[payment_terms_template_id])

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    group_same_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_internal_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    credit_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    credit_to = relationship("Account", foreign_keys=[credit_to_id])

    party_account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_opening: Mapped[Optional[PurchaseInvoiceIsOpening]] = mapped_column(

        SAEnum(PurchaseInvoiceIsOpening, native_enum=False, length=3, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    against_expense_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[Optional[PurchaseInvoiceStatus]] = mapped_column(

        SAEnum(PurchaseInvoiceStatus, native_enum=False, length=17, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    inter_company_invoice_reference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    from_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    auto_repeat: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    unrealized_profit_loss_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    unrealized_profit_loss_account = relationship("Account", foreign_keys=[unrealized_profit_loss_account_id])

    set_from_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    per_received: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ignore_default_payment_terms_template: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    subscription: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    incoterm: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    named_place: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    only_include_allocated_payments: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    use_company_roundoff_cost_center: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    use_transaction_date_exchange_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    supplier_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    update_outstanding_for_self: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    sender: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dispatch_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    dispatch_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    claimed_landed_cost_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_withholding_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_withholding_group = relationship("TaxWithholdingGroup", foreign_keys=[tax_withholding_group_id])

    ignore_tax_withholding_threshold: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    override_tax_withholding_entries: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    items = relationship(

        PurchaseInvoiceItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PurchaseInvoiceItem.idx,

        passive_deletes=True,

    )

    pricing_rules = relationship(

        PricingRuleDetail,

        primaryjoin="and_(PurchaseInvoice.id == foreign(PricingRuleDetail.parent_id), PricingRuleDetail.parenttype == 'Purchase Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=PricingRuleDetail.idx,

        overlaps="pricing_rules",

    )

    advances = relationship(

        PurchaseInvoiceAdvance,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PurchaseInvoiceAdvance.idx,

        passive_deletes=True,

    )

    tax_withholding_entries = relationship(

        TaxWithholdingEntry,

        primaryjoin="and_(PurchaseInvoice.id == foreign(TaxWithholdingEntry.parent_id), TaxWithholdingEntry.parenttype == 'Purchase Invoice')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=TaxWithholdingEntry.idx,

        overlaps="tax_withholding_entries",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PurchaseInvoice id={self.id}>"

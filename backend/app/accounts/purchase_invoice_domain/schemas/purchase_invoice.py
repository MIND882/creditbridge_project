"""Pydantic v2 schemas for PurchaseInvoice."""





from __future__ import annotations

from app.accounts.purchase_invoice_domain.models.purchase_invoice import (

    PurchaseInvoiceApplyDiscountOn,

    PurchaseInvoiceIsOpening,

    PurchaseInvoiceNamingSeries,

    PurchaseInvoiceStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.accounts.purchase_invoice_item_domain.schemas.purchase_invoice_item import (

    PurchaseInvoiceItemCreate,

    PurchaseInvoiceItemRead,

)

from app.accounts.purchase_invoice_advance_domain.schemas.purchase_invoice_advance import (

    PurchaseInvoiceAdvanceCreate,

    PurchaseInvoiceAdvanceRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.pos_invoice_item_domain.schemas.pos_invoice_item import (

    POSInvoiceItemCreate,

    POSInvoiceItemRead,

)

from app.accounts.pricing_rule_detail_domain.schemas.pricing_rule_detail import (

    PricingRuleDetailCreate,

    PricingRuleDetailRead,

)

from app.accounts.sales_invoice_advance_domain.schemas.sales_invoice_advance import (

    SalesInvoiceAdvanceCreate,

    SalesInvoiceAdvanceRead,

)

from app.accounts.tax_withholding_entry_domain.schemas.tax_withholding_entry import (

    TaxWithholdingEntryCreate,

    TaxWithholdingEntryRead,

)



__all__ = [

    "PurchaseInvoiceCreate",

    "PurchaseInvoiceUpdate",

    "PurchaseInvoiceRead",

    "PurchaseInvoiceListResponse",

]





class PurchaseInvoiceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    title: Optional[str] = None

    naming_series: PurchaseInvoiceNamingSeries

    supplier: str

    supplier_name: Optional[str] = None

    due_date: Optional[dt.date] = None

    is_paid: Optional[bool] = None

    is_return: Optional[bool] = None

    apply_tds: Optional[bool] = None

    cost_center_id: Optional[uuid.UUID] = None

    posting_date: dt.date

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    amended_from: Optional[str] = None

    on_hold: Optional[bool] = None

    release_date: Optional[dt.date] = None

    hold_comment: Optional[str] = None

    bill_no: Optional[str] = None

    bill_date: Optional[dt.date] = None

    return_against: Optional[str] = None

    update_billed_amount_in_purchase_order: Optional[bool] = None

    update_billed_amount_in_purchase_receipt: Optional[bool] = None

    supplier_address: Optional[str] = None

    address_display: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    buying_price_list: Optional[str] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    set_warehouse: Optional[str] = None

    rejected_warehouse: Optional[str] = None

    is_subcontracted: Optional[bool] = None

    update_stock: Optional[bool] = None

    scan_barcode: Optional[str] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    tax_category_id: Optional[uuid.UUID] = None

    shipping_rule: Optional[str] = None

    taxes_and_charges: Optional[str] = None

    other_charges_calculation: Optional[str] = None

    base_taxes_and_charges_added: Optional[Decimal] = None

    base_taxes_and_charges_deducted: Optional[Decimal] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    taxes_and_charges_added: Optional[Decimal] = None

    taxes_and_charges_deducted: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[PurchaseInvoiceApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_grand_total: Optional[Decimal] = None

    base_rounding_adjustment: Optional[Decimal] = None

    base_rounded_total: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    grand_total: Optional[Decimal] = None

    rounding_adjustment: Optional[Decimal] = None

    rounded_total: Optional[Decimal] = None

    in_words: Optional[str] = None

    total_advance: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    disable_rounded_total: Optional[bool] = None

    mode_of_payment_id: Optional[uuid.UUID] = None

    cash_bank_account_id: Optional[uuid.UUID] = None

    clearance_date: Optional[dt.date] = None

    paid_amount: Optional[Decimal] = None

    base_paid_amount: Optional[Decimal] = None

    write_off_amount: Optional[Decimal] = None

    base_write_off_amount: Optional[Decimal] = None

    write_off_account_id: Optional[uuid.UUID] = None

    write_off_cost_center_id: Optional[uuid.UUID] = None

    allocate_advances_automatically: Optional[bool] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: Optional[bool] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    is_internal_supplier: Optional[bool] = None

    credit_to_id: Optional[uuid.UUID] = None

    party_account_currency: Optional[str] = None

    is_opening: Optional[PurchaseInvoiceIsOpening] = None

    against_expense_account: Optional[str] = None

    status: Optional[PurchaseInvoiceStatus] = None

    inter_company_invoice_reference: Optional[str] = None

    remarks: Optional[str] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    project: Optional[str] = None

    unrealized_profit_loss_account_id: Optional[uuid.UUID] = None

    set_from_warehouse: Optional[str] = None

    supplier_warehouse: Optional[str] = None

    per_received: Optional[Decimal] = None

    ignore_default_payment_terms_template: Optional[bool] = None

    subscription: Optional[str] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    only_include_allocated_payments: Optional[bool] = None

    use_company_roundoff_cost_center: Optional[bool] = None

    use_transaction_date_exchange_rate: Optional[bool] = None

    supplier_group: Optional[str] = None

    update_outstanding_for_self: Optional[bool] = None

    sender: Optional[str] = None

    dispatch_address_display: Optional[str] = None

    dispatch_address: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    claimed_landed_cost_amount: Optional[Decimal] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    ignore_tax_withholding_threshold: Optional[bool] = None

    override_tax_withholding_entries: Optional[bool] = None



    items: list[PurchaseInvoiceItemCreate] = []



    pricing_rules: list[PricingRuleDetailCreate] = []



    advances: list[PurchaseInvoiceAdvanceCreate] = []



    tax_withholding_entries: list[TaxWithholdingEntryCreate] = []





class PurchaseInvoiceCreate(PurchaseInvoiceBase):

    pass





class PurchaseInvoiceUpdate(InputSchema):

    """A partial update."""



    title: Optional[str] = None

    naming_series: Optional[PurchaseInvoiceNamingSeries] = None

    supplier: Optional[str] = None

    supplier_name: Optional[str] = None

    due_date: Optional[dt.date] = None

    is_paid: Optional[bool] = None

    is_return: Optional[bool] = None

    apply_tds: Optional[bool] = None

    cost_center_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    amended_from: Optional[str] = None

    on_hold: Optional[bool] = None

    release_date: Optional[dt.date] = None

    hold_comment: Optional[str] = None

    bill_no: Optional[str] = None

    bill_date: Optional[dt.date] = None

    return_against: Optional[str] = None

    update_billed_amount_in_purchase_order: Optional[bool] = None

    update_billed_amount_in_purchase_receipt: Optional[bool] = None

    supplier_address: Optional[str] = None

    address_display: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    buying_price_list: Optional[str] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    set_warehouse: Optional[str] = None

    rejected_warehouse: Optional[str] = None

    is_subcontracted: Optional[bool] = None

    update_stock: Optional[bool] = None

    scan_barcode: Optional[str] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    tax_category_id: Optional[uuid.UUID] = None

    shipping_rule: Optional[str] = None

    taxes_and_charges: Optional[str] = None

    other_charges_calculation: Optional[str] = None

    base_taxes_and_charges_added: Optional[Decimal] = None

    base_taxes_and_charges_deducted: Optional[Decimal] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    taxes_and_charges_added: Optional[Decimal] = None

    taxes_and_charges_deducted: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[PurchaseInvoiceApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_grand_total: Optional[Decimal] = None

    base_rounding_adjustment: Optional[Decimal] = None

    base_rounded_total: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    grand_total: Optional[Decimal] = None

    rounding_adjustment: Optional[Decimal] = None

    rounded_total: Optional[Decimal] = None

    in_words: Optional[str] = None

    total_advance: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    disable_rounded_total: Optional[bool] = None

    mode_of_payment_id: Optional[uuid.UUID] = None

    cash_bank_account_id: Optional[uuid.UUID] = None

    clearance_date: Optional[dt.date] = None

    paid_amount: Optional[Decimal] = None

    base_paid_amount: Optional[Decimal] = None

    write_off_amount: Optional[Decimal] = None

    base_write_off_amount: Optional[Decimal] = None

    write_off_account_id: Optional[uuid.UUID] = None

    write_off_cost_center_id: Optional[uuid.UUID] = None

    allocate_advances_automatically: Optional[bool] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: Optional[bool] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    is_internal_supplier: Optional[bool] = None

    credit_to_id: Optional[uuid.UUID] = None

    party_account_currency: Optional[str] = None

    is_opening: Optional[PurchaseInvoiceIsOpening] = None

    against_expense_account: Optional[str] = None

    status: Optional[PurchaseInvoiceStatus] = None

    inter_company_invoice_reference: Optional[str] = None

    remarks: Optional[str] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    project: Optional[str] = None

    unrealized_profit_loss_account_id: Optional[uuid.UUID] = None

    set_from_warehouse: Optional[str] = None

    supplier_warehouse: Optional[str] = None

    per_received: Optional[Decimal] = None

    ignore_default_payment_terms_template: Optional[bool] = None

    subscription: Optional[str] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    only_include_allocated_payments: Optional[bool] = None

    use_company_roundoff_cost_center: Optional[bool] = None

    use_transaction_date_exchange_rate: Optional[bool] = None

    supplier_group: Optional[str] = None

    update_outstanding_for_self: Optional[bool] = None

    sender: Optional[str] = None

    dispatch_address_display: Optional[str] = None

    dispatch_address: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    claimed_landed_cost_amount: Optional[Decimal] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    ignore_tax_withholding_threshold: Optional[bool] = None

    override_tax_withholding_entries: Optional[bool] = None

    items: Optional[list[PurchaseInvoiceItemCreate]] = None

    pricing_rules: Optional[list[PricingRuleDetailCreate]] = None

    advances: Optional[list[PurchaseInvoiceAdvanceCreate]] = None

    tax_withholding_entries: Optional[list[TaxWithholdingEntryCreate]] = None





class PurchaseInvoiceRead(ReadSchema):

    id: uuid.UUID

    name: str

    title: Optional[str] = None

    naming_series: PurchaseInvoiceNamingSeries

    supplier: str

    supplier_name: Optional[str] = None

    due_date: Optional[dt.date] = None

    is_paid: bool

    is_return: bool

    apply_tds: bool

    cost_center_id: Optional[uuid.UUID] = None

    posting_date: dt.date

    posting_time: Optional[dt.time] = None

    set_posting_time: bool

    amended_from: Optional[str] = None

    on_hold: bool

    release_date: Optional[dt.date] = None

    hold_comment: Optional[str] = None

    bill_no: Optional[str] = None

    bill_date: Optional[dt.date] = None

    return_against: Optional[str] = None

    update_billed_amount_in_purchase_order: bool

    update_billed_amount_in_purchase_receipt: bool

    supplier_address: Optional[str] = None

    address_display: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    buying_price_list: Optional[str] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: bool

    set_warehouse: Optional[str] = None

    rejected_warehouse: Optional[str] = None

    is_subcontracted: bool

    update_stock: bool

    scan_barcode: Optional[str] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    tax_category_id: Optional[uuid.UUID] = None

    shipping_rule: Optional[str] = None

    taxes_and_charges: Optional[str] = None

    other_charges_calculation: Optional[str] = None

    base_taxes_and_charges_added: Optional[Decimal] = None

    base_taxes_and_charges_deducted: Optional[Decimal] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    taxes_and_charges_added: Optional[Decimal] = None

    taxes_and_charges_deducted: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[PurchaseInvoiceApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_grand_total: Optional[Decimal] = None

    base_rounding_adjustment: Optional[Decimal] = None

    base_rounded_total: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    grand_total: Optional[Decimal] = None

    rounding_adjustment: Optional[Decimal] = None

    rounded_total: Optional[Decimal] = None

    in_words: Optional[str] = None

    total_advance: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    disable_rounded_total: bool

    mode_of_payment_id: Optional[uuid.UUID] = None

    cash_bank_account_id: Optional[uuid.UUID] = None

    clearance_date: Optional[dt.date] = None

    paid_amount: Optional[Decimal] = None

    base_paid_amount: Optional[Decimal] = None

    write_off_amount: Optional[Decimal] = None

    base_write_off_amount: Optional[Decimal] = None

    write_off_account_id: Optional[uuid.UUID] = None

    write_off_cost_center_id: Optional[uuid.UUID] = None

    allocate_advances_automatically: bool

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: bool

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    is_internal_supplier: bool

    credit_to_id: uuid.UUID

    party_account_currency: Optional[str] = None

    is_opening: Optional[PurchaseInvoiceIsOpening] = None

    against_expense_account: Optional[str] = None

    status: Optional[PurchaseInvoiceStatus] = None

    inter_company_invoice_reference: Optional[str] = None

    remarks: Optional[str] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    project: Optional[str] = None

    unrealized_profit_loss_account_id: Optional[uuid.UUID] = None

    set_from_warehouse: Optional[str] = None

    supplier_warehouse: Optional[str] = None

    per_received: Optional[Decimal] = None

    ignore_default_payment_terms_template: bool

    subscription: Optional[str] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    only_include_allocated_payments: bool

    use_company_roundoff_cost_center: bool

    use_transaction_date_exchange_rate: bool

    supplier_group: Optional[str] = None

    update_outstanding_for_self: bool

    sender: Optional[str] = None

    dispatch_address_display: Optional[str] = None

    dispatch_address: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    claimed_landed_cost_amount: Optional[Decimal] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    ignore_tax_withholding_threshold: bool

    override_tax_withholding_entries: bool

    items: list[PurchaseInvoiceItemRead] = []

    pricing_rules: list[PricingRuleDetailRead] = []

    advances: list[PurchaseInvoiceAdvanceRead] = []

    tax_withholding_entries: list[TaxWithholdingEntryRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





PurchaseInvoiceListResponse = Page[PurchaseInvoiceRead]

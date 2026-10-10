"""Pydantic v2 schemas for POSInvoice."""





from __future__ import annotations

from app.accounts.pos_invoice_domain.models.pos_invoice import (

    POSInvoiceApplyDiscountOn,

    POSInvoiceIsOpening,

    POSInvoiceNamingSeries,

    POSInvoiceStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.accounts.sales_invoice_payment_domain.schemas.sales_invoice_payment import (

    SalesInvoicePaymentCreate,

    SalesInvoicePaymentRead,

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

from app.accounts.sales_invoice_timesheet_domain.schemas.sales_invoice_timesheet import (

    SalesInvoiceTimesheetCreate,

    SalesInvoiceTimesheetRead,

)

from app.accounts.sales_invoice_advance_domain.schemas.sales_invoice_advance import (

    SalesInvoiceAdvanceCreate,

    SalesInvoiceAdvanceRead,

)

from app.accounts.cashier_closing_payments_domain.schemas.cashier_closing_payments import (

    CashierClosingPaymentsCreate,

    CashierClosingPaymentsRead,

)



__all__ = [

    "POSInvoiceCreate",

    "POSInvoiceUpdate",

    "POSInvoiceRead",

    "POSInvoiceListResponse",

]





class POSInvoiceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: POSInvoiceNamingSeries

    customer: Optional[str] = None

    customer_name: Optional[str] = None

    is_pos: Optional[bool] = None

    pos_profile: Optional[str] = None

    is_return: Optional[bool] = None

    posting_date: dt.date

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    due_date: Optional[dt.date] = None

    amended_from: Optional[str] = None

    return_against: Optional[str] = None

    update_billed_amount_in_sales_order: Optional[bool] = None

    project: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    po_no: Optional[str] = None

    po_date: Optional[dt.date] = None

    customer_address: Optional[str] = None

    address_display: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    territory: Optional[str] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    currency: str

    conversion_rate: Optional[Decimal] = None

    selling_price_list: str

    price_list_currency: str

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    set_warehouse: Optional[str] = None

    update_stock: Optional[bool] = None

    scan_barcode: Optional[str] = None

    total_billing_amount: Optional[Decimal] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    taxes_and_charges: Optional[str] = None

    shipping_rule: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    other_charges_calculation: Optional[str] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    loyalty_points: Optional[int] = None

    loyalty_amount: Optional[Decimal] = None

    redeem_loyalty_points: Optional[bool] = None

    loyalty_program: Optional[str] = None

    loyalty_redemption_account_id: Optional[uuid.UUID] = None

    loyalty_redemption_cost_center_id: Optional[uuid.UUID] = None

    apply_discount_on: Optional[POSInvoiceApplyDiscountOn] = None

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

    allocate_advances_automatically: Optional[bool] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    cash_bank_account_id: Optional[uuid.UUID] = None

    base_paid_amount: Optional[Decimal] = None

    paid_amount: Optional[Decimal] = None

    base_change_amount: Optional[Decimal] = None

    change_amount: Optional[Decimal] = None

    account_for_change_amount_id: Optional[uuid.UUID] = None

    write_off_amount: Optional[Decimal] = None

    base_write_off_amount: Optional[Decimal] = None

    write_off_outstanding_amount_automatically: Optional[bool] = None

    write_off_account_id: Optional[uuid.UUID] = None

    write_off_cost_center_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: Optional[bool] = None

    language: Optional[str] = None

    select_print_heading: Optional[str] = None

    inter_company_invoice_reference: Optional[str] = None

    customer_group: Optional[str] = None

    is_discounted: Optional[bool] = None

    status: Optional[POSInvoiceStatus] = None

    debit_to_id: uuid.UUID

    party_account_currency: Optional[str] = None

    is_opening: Optional[POSInvoiceIsOpening] = None

    remarks: Optional[str] = None

    sales_partner: Optional[str] = None

    commission_rate: Optional[Decimal] = None

    total_commission: Optional[Decimal] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    against_income_account: Optional[str] = None

    consolidated_invoice: Optional[str] = None

    coupon_code: Optional[str] = None

    amount_eligible_for_commission: Optional[Decimal] = None

    update_billed_amount_in_delivery_note: Optional[bool] = None

    utm_medium: Optional[str] = None

    utm_campaign: Optional[str] = None

    utm_source: Optional[str] = None

    company_contact_person: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    title: Optional[str] = None



    items: list[POSInvoiceItemCreate] = []



    pricing_rules: list[PricingRuleDetailCreate] = []



    timesheets: list[SalesInvoiceTimesheetCreate] = []



    advances: list[SalesInvoiceAdvanceCreate] = []



    payments: list[SalesInvoicePaymentCreate] = []





class POSInvoiceCreate(POSInvoiceBase):

    pass





class POSInvoiceUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[POSInvoiceNamingSeries] = None

    customer: Optional[str] = None

    customer_name: Optional[str] = None

    is_pos: Optional[bool] = None

    pos_profile: Optional[str] = None

    is_return: Optional[bool] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    due_date: Optional[dt.date] = None

    amended_from: Optional[str] = None

    return_against: Optional[str] = None

    update_billed_amount_in_sales_order: Optional[bool] = None

    project: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    po_no: Optional[str] = None

    po_date: Optional[dt.date] = None

    customer_address: Optional[str] = None

    address_display: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    territory: Optional[str] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    selling_price_list: Optional[str] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    set_warehouse: Optional[str] = None

    update_stock: Optional[bool] = None

    scan_barcode: Optional[str] = None

    total_billing_amount: Optional[Decimal] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    taxes_and_charges: Optional[str] = None

    shipping_rule: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    other_charges_calculation: Optional[str] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    loyalty_points: Optional[int] = None

    loyalty_amount: Optional[Decimal] = None

    redeem_loyalty_points: Optional[bool] = None

    loyalty_program: Optional[str] = None

    loyalty_redemption_account_id: Optional[uuid.UUID] = None

    loyalty_redemption_cost_center_id: Optional[uuid.UUID] = None

    apply_discount_on: Optional[POSInvoiceApplyDiscountOn] = None

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

    allocate_advances_automatically: Optional[bool] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    cash_bank_account_id: Optional[uuid.UUID] = None

    base_paid_amount: Optional[Decimal] = None

    paid_amount: Optional[Decimal] = None

    base_change_amount: Optional[Decimal] = None

    change_amount: Optional[Decimal] = None

    account_for_change_amount_id: Optional[uuid.UUID] = None

    write_off_amount: Optional[Decimal] = None

    base_write_off_amount: Optional[Decimal] = None

    write_off_outstanding_amount_automatically: Optional[bool] = None

    write_off_account_id: Optional[uuid.UUID] = None

    write_off_cost_center_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: Optional[bool] = None

    language: Optional[str] = None

    select_print_heading: Optional[str] = None

    inter_company_invoice_reference: Optional[str] = None

    customer_group: Optional[str] = None

    is_discounted: Optional[bool] = None

    status: Optional[POSInvoiceStatus] = None

    debit_to_id: Optional[uuid.UUID] = None

    party_account_currency: Optional[str] = None

    is_opening: Optional[POSInvoiceIsOpening] = None

    remarks: Optional[str] = None

    sales_partner: Optional[str] = None

    commission_rate: Optional[Decimal] = None

    total_commission: Optional[Decimal] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    against_income_account: Optional[str] = None

    consolidated_invoice: Optional[str] = None

    coupon_code: Optional[str] = None

    amount_eligible_for_commission: Optional[Decimal] = None

    update_billed_amount_in_delivery_note: Optional[bool] = None

    utm_medium: Optional[str] = None

    utm_campaign: Optional[str] = None

    utm_source: Optional[str] = None

    company_contact_person: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    title: Optional[str] = None

    items: Optional[list[POSInvoiceItemCreate]] = None

    pricing_rules: Optional[list[PricingRuleDetailCreate]] = None

    timesheets: Optional[list[SalesInvoiceTimesheetCreate]] = None

    advances: Optional[list[SalesInvoiceAdvanceCreate]] = None

    payments: Optional[list[SalesInvoicePaymentCreate]] = None





class POSInvoiceRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: POSInvoiceNamingSeries

    customer: Optional[str] = None

    customer_name: Optional[str] = None

    is_pos: bool

    pos_profile: Optional[str] = None

    is_return: bool

    posting_date: dt.date

    posting_time: Optional[dt.time] = None

    set_posting_time: bool

    due_date: Optional[dt.date] = None

    amended_from: Optional[str] = None

    return_against: Optional[str] = None

    update_billed_amount_in_sales_order: bool

    project: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    po_no: Optional[str] = None

    po_date: Optional[dt.date] = None

    customer_address: Optional[str] = None

    address_display: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    territory: Optional[str] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    currency: str

    conversion_rate: Decimal

    selling_price_list: str

    price_list_currency: str

    plc_conversion_rate: Decimal

    ignore_pricing_rule: bool

    set_warehouse: Optional[str] = None

    update_stock: bool

    scan_barcode: Optional[str] = None

    total_billing_amount: Optional[Decimal] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Decimal

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    taxes_and_charges: Optional[str] = None

    shipping_rule: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    other_charges_calculation: Optional[str] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    loyalty_points: Optional[int] = None

    loyalty_amount: Optional[Decimal] = None

    redeem_loyalty_points: bool

    loyalty_program: Optional[str] = None

    loyalty_redemption_account_id: Optional[uuid.UUID] = None

    loyalty_redemption_cost_center_id: Optional[uuid.UUID] = None

    apply_discount_on: Optional[POSInvoiceApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_grand_total: Decimal

    base_rounding_adjustment: Optional[Decimal] = None

    base_rounded_total: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    grand_total: Decimal

    rounding_adjustment: Optional[Decimal] = None

    rounded_total: Optional[Decimal] = None

    in_words: Optional[str] = None

    total_advance: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    allocate_advances_automatically: bool

    payment_terms_template_id: Optional[uuid.UUID] = None

    cash_bank_account_id: Optional[uuid.UUID] = None

    base_paid_amount: Optional[Decimal] = None

    paid_amount: Optional[Decimal] = None

    base_change_amount: Optional[Decimal] = None

    change_amount: Optional[Decimal] = None

    account_for_change_amount_id: Optional[uuid.UUID] = None

    write_off_amount: Optional[Decimal] = None

    base_write_off_amount: Optional[Decimal] = None

    write_off_outstanding_amount_automatically: bool

    write_off_account_id: Optional[uuid.UUID] = None

    write_off_cost_center_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: bool

    language: Optional[str] = None

    select_print_heading: Optional[str] = None

    inter_company_invoice_reference: Optional[str] = None

    customer_group: Optional[str] = None

    is_discounted: bool

    status: Optional[POSInvoiceStatus] = None

    debit_to_id: uuid.UUID

    party_account_currency: Optional[str] = None

    is_opening: Optional[POSInvoiceIsOpening] = None

    remarks: Optional[str] = None

    sales_partner: Optional[str] = None

    commission_rate: Optional[Decimal] = None

    total_commission: Optional[Decimal] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    against_income_account: Optional[str] = None

    consolidated_invoice: Optional[str] = None

    coupon_code: Optional[str] = None

    amount_eligible_for_commission: Optional[Decimal] = None

    update_billed_amount_in_delivery_note: bool

    utm_medium: Optional[str] = None

    utm_campaign: Optional[str] = None

    utm_source: Optional[str] = None

    company_contact_person: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    title: Optional[str] = None

    items: list[POSInvoiceItemRead] = []

    pricing_rules: list[PricingRuleDetailRead] = []

    timesheets: list[SalesInvoiceTimesheetRead] = []

    advances: list[SalesInvoiceAdvanceRead] = []

    payments: list[SalesInvoicePaymentRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





POSInvoiceListResponse = Page[POSInvoiceRead]

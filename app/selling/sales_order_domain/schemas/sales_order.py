"""Pydantic v2 schemas for SalesOrder."""





from __future__ import annotations

from app.selling.sales_order_domain.models.sales_order import (

    SalesOrderNamingSeries,

    SalesOrderOrderType,

    SalesOrderApplyDiscountOn,

    SalesOrderStatus,

    SalesOrderDeliveryStatus,

    SalesOrderBillingStatus,

    SalesOrderAdvancePaymentStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.selling.sales_order_item_domain.schemas.sales_order_item import (

    SalesOrderItemCreate,

    SalesOrderItemRead,

)

from app.selling.delivery_schedule_item_domain.schemas.delivery_schedule_item import (

    DeliveryScheduleItemCreate,

    DeliveryScheduleItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesOrderCreate",

    "SalesOrderUpdate",

    "SalesOrderRead",

    "SalesOrderListResponse",

]





class SalesOrderBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    company: str

    naming_series: SalesOrderNamingSeries

    customer_id: uuid.UUID

    customer_name: Optional[str] = None

    order_type: SalesOrderOrderType

    transaction_date: dt.date

    transaction_time: Optional[dt.time] = None

    delivery_date: Optional[dt.date] = None

    tax_id: Optional[str] = None

    skip_delivery_note: Optional[bool] = None

    has_unit_price_items: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    currency: str

    conversion_rate: Decimal

    selling_price_list_id: uuid.UUID

    price_list_currency: str

    plc_conversion_rate: Decimal

    ignore_pricing_rule: Optional[bool] = None

    scan_barcode: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    reserve_stock: Optional[bool] = None

    total_qty: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    tax_category_id: Optional[uuid.UUID] = None

    taxes_and_charges_id: Optional[uuid.UUID] = None

    shipping_rule_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    grand_total: Optional[Decimal] = None

    in_words: Optional[str] = None

    disable_rounded_total: Optional[bool] = None

    rounding_adjustment: Optional[Decimal] = None

    rounded_total: Optional[Decimal] = None

    base_grand_total: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    base_rounding_adjustment: Optional[Decimal] = None

    base_rounded_total: Optional[Decimal] = None

    advance_paid: Optional[Decimal] = None

    apply_discount_on: Optional[SalesOrderApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    coupon_code_id: Optional[uuid.UUID] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    other_charges_calculation: Optional[str] = None

    customer_address: Optional[str] = None

    address_display: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_phone: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    dispatch_address_name: Optional[str] = None

    dispatch_address: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    company_contact_person: Optional[str] = None

    ignore_default_payment_terms_template: Optional[bool] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    status: SalesOrderStatus

    delivery_status: Optional[SalesOrderDeliveryStatus] = None

    per_delivered: Optional[Decimal] = None

    per_billed: Optional[Decimal] = None

    per_picked: Optional[Decimal] = None

    billing_status: Optional[SalesOrderBillingStatus] = None

    advance_payment_status: Optional[SalesOrderAdvancePaymentStatus] = None

    sales_partner: Optional[str] = None

    amount_eligible_for_commission: Optional[Decimal] = None

    commission_rate: Optional[Decimal] = None

    total_commission: Optional[Decimal] = None

    loyalty_points: Optional[int] = None

    loyalty_amount: Optional[Decimal] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: Optional[bool] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    utm_source: Optional[str] = None

    utm_medium: Optional[str] = None

    utm_campaign: Optional[str] = None

    utm_content: Optional[str] = None

    is_internal_customer: Optional[bool] = None

    po_no: Optional[str] = None

    po_date: Optional[dt.date] = None

    represents_company: Optional[str] = None

    title: Optional[str] = None

    inter_company_order_reference_id: Optional[uuid.UUID] = None

    party_account_currency: Optional[str] = None

    items: list[SalesOrderItemCreate] = []

    delivery_schedule: list[DeliveryScheduleItemCreate] = []





class SalesOrderCreate(SalesOrderBase):

    pass





class SalesOrderUpdate(InputSchema):

    """A partial update."""



    company: Optional[str] = None

    naming_series: Optional[SalesOrderNamingSeries] = None

    customer_id: Optional[uuid.UUID] = None

    customer_name: Optional[str] = None

    order_type: Optional[SalesOrderOrderType] = None

    transaction_date: Optional[dt.date] = None

    transaction_time: Optional[dt.time] = None

    delivery_date: Optional[dt.date] = None

    tax_id: Optional[str] = None

    skip_delivery_note: Optional[bool] = None

    has_unit_price_items: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    selling_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    scan_barcode: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    reserve_stock: Optional[bool] = None

    total_qty: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    tax_category_id: Optional[uuid.UUID] = None

    taxes_and_charges_id: Optional[uuid.UUID] = None

    shipping_rule_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    grand_total: Optional[Decimal] = None

    in_words: Optional[str] = None

    disable_rounded_total: Optional[bool] = None

    rounding_adjustment: Optional[Decimal] = None

    rounded_total: Optional[Decimal] = None

    base_grand_total: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    base_rounding_adjustment: Optional[Decimal] = None

    base_rounded_total: Optional[Decimal] = None

    advance_paid: Optional[Decimal] = None

    apply_discount_on: Optional[SalesOrderApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    coupon_code_id: Optional[uuid.UUID] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    other_charges_calculation: Optional[str] = None

    customer_address: Optional[str] = None

    address_display: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_phone: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    dispatch_address_name: Optional[str] = None

    dispatch_address: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    company_contact_person: Optional[str] = None

    ignore_default_payment_terms_template: Optional[bool] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    status: Optional[SalesOrderStatus] = None

    delivery_status: Optional[SalesOrderDeliveryStatus] = None

    per_delivered: Optional[Decimal] = None

    per_billed: Optional[Decimal] = None

    per_picked: Optional[Decimal] = None

    billing_status: Optional[SalesOrderBillingStatus] = None

    advance_payment_status: Optional[SalesOrderAdvancePaymentStatus] = None

    sales_partner: Optional[str] = None

    amount_eligible_for_commission: Optional[Decimal] = None

    commission_rate: Optional[Decimal] = None

    total_commission: Optional[Decimal] = None

    loyalty_points: Optional[int] = None

    loyalty_amount: Optional[Decimal] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: Optional[bool] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    utm_source: Optional[str] = None

    utm_medium: Optional[str] = None

    utm_campaign: Optional[str] = None

    utm_content: Optional[str] = None

    is_internal_customer: Optional[bool] = None

    po_no: Optional[str] = None

    po_date: Optional[dt.date] = None

    represents_company: Optional[str] = None

    title: Optional[str] = None

    inter_company_order_reference_id: Optional[uuid.UUID] = None

    party_account_currency: Optional[str] = None

    items: Optional[list[SalesOrderItemCreate]] = None

    delivery_schedule: Optional[list[DeliveryScheduleItemCreate]] = None





class SalesOrderRead(ReadSchema):

    id: uuid.UUID

    name: str

    company: str

    naming_series: Optional[SalesOrderNamingSeries] = None

    customer_id: Optional[uuid.UUID] = None

    customer_name: Optional[str] = None

    order_type: Optional[SalesOrderOrderType] = None

    transaction_date: Optional[dt.date] = None

    transaction_time: Optional[dt.time] = None

    delivery_date: Optional[dt.date] = None

    tax_id: Optional[str] = None

    skip_delivery_note: Optional[bool] = None

    has_unit_price_items: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    currency: str

    conversion_rate: Optional[Decimal] = None

    selling_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: str

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    scan_barcode: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    reserve_stock: Optional[bool] = None

    total_qty: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    tax_category_id: Optional[uuid.UUID] = None

    taxes_and_charges_id: Optional[uuid.UUID] = None

    shipping_rule_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    grand_total: Optional[Decimal] = None

    in_words: Optional[str] = None

    disable_rounded_total: Optional[bool] = None

    rounding_adjustment: Optional[Decimal] = None

    rounded_total: Optional[Decimal] = None

    base_grand_total: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    base_rounding_adjustment: Optional[Decimal] = None

    base_rounded_total: Optional[Decimal] = None

    advance_paid: Optional[Decimal] = None

    apply_discount_on: Optional[SalesOrderApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    coupon_code_id: Optional[uuid.UUID] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    other_charges_calculation: Optional[str] = None

    customer_address: Optional[str] = None

    address_display: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_phone: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    dispatch_address_name: Optional[str] = None

    dispatch_address: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    company_contact_person: Optional[str] = None

    ignore_default_payment_terms_template: Optional[bool] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    status: Optional[SalesOrderStatus] = None

    delivery_status: Optional[SalesOrderDeliveryStatus] = None

    per_delivered: Optional[Decimal] = None

    per_billed: Optional[Decimal] = None

    per_picked: Optional[Decimal] = None

    billing_status: Optional[SalesOrderBillingStatus] = None

    advance_payment_status: Optional[SalesOrderAdvancePaymentStatus] = None

    sales_partner: Optional[str] = None

    amount_eligible_for_commission: Optional[Decimal] = None

    commission_rate: Optional[Decimal] = None

    total_commission: Optional[Decimal] = None

    loyalty_points: Optional[int] = None

    loyalty_amount: Optional[Decimal] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: Optional[bool] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    utm_source: Optional[str] = None

    utm_medium: Optional[str] = None

    utm_campaign: Optional[str] = None

    utm_content: Optional[str] = None

    is_internal_customer: Optional[bool] = None

    po_no: Optional[str] = None

    po_date: Optional[dt.date] = None

    represents_company: Optional[str] = None

    title: Optional[str] = None

    inter_company_order_reference_id: Optional[uuid.UUID] = None

    party_account_currency: Optional[str] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[SalesOrderItemRead] = []

    delivery_schedule: list[DeliveryScheduleItemRead] = []





SalesOrderListResponse = Page[SalesOrderRead]

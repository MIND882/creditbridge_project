"""Pydantic v2 schemas for Quotation."""





from __future__ import annotations

from app.selling.quotation_domain.models.quotation import (

    QuotationNamingSeries,

    QuotationOrderType,

    QuotationApplyDiscountOn,

    QuotationStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.selling.quotation_item_domain.schemas.quotation_item import (

    QuotationItemCreate,

    QuotationItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "QuotationCreate",

    "QuotationUpdate",

    "QuotationRead",

    "QuotationListResponse",

]





class QuotationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: QuotationNamingSeries

    quotation_to: str

    party_name: Optional[str] = None

    customer_name: Optional[str] = None

    transaction_date: dt.date

    valid_till: Optional[dt.date] = None

    order_type: QuotationOrderType

    company: str

    has_unit_price_items: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    currency: str

    conversion_rate: Decimal

    selling_price_list_id: uuid.UUID

    price_list_currency: str

    plc_conversion_rate: Decimal

    ignore_pricing_rule: Optional[bool] = None

    scan_barcode: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

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

    rounded_total: Optional[Decimal] = None

    rounding_adjustment: Optional[Decimal] = None

    disable_rounded_total: Optional[bool] = None

    base_grand_total: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    base_rounded_total: Optional[Decimal] = None

    base_rounding_adjustment: Optional[Decimal] = None

    apply_discount_on: Optional[QuotationApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    coupon_code_id: Optional[uuid.UUID] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    referral_sales_partner: Optional[str] = None

    other_charges_calculation: Optional[str] = None

    customer_address: Optional[str] = None

    address_display: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    company_contact_person: Optional[str] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    auto_repeat: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: Optional[bool] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    order_lost_reason: Optional[str] = None

    utm_source: Optional[str] = None

    utm_medium: Optional[str] = None

    utm_campaign: Optional[str] = None

    utm_content: Optional[str] = None

    status: QuotationStatus

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    title: Optional[str] = None

    opportunity: Optional[str] = None

    enq_det: Optional[str] = None

    supplier_quotation_id: Optional[uuid.UUID] = None

    items: list[QuotationItemCreate] = []





class QuotationCreate(QuotationBase):

    pass





class QuotationUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[QuotationNamingSeries] = None

    quotation_to: Optional[str] = None

    party_name: Optional[str] = None

    customer_name: Optional[str] = None

    transaction_date: Optional[dt.date] = None

    valid_till: Optional[dt.date] = None

    order_type: Optional[QuotationOrderType] = None

    company: Optional[str] = None

    has_unit_price_items: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    selling_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    scan_barcode: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

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

    rounded_total: Optional[Decimal] = None

    rounding_adjustment: Optional[Decimal] = None

    disable_rounded_total: Optional[bool] = None

    base_grand_total: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    base_rounded_total: Optional[Decimal] = None

    base_rounding_adjustment: Optional[Decimal] = None

    apply_discount_on: Optional[QuotationApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    coupon_code_id: Optional[uuid.UUID] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    referral_sales_partner: Optional[str] = None

    other_charges_calculation: Optional[str] = None

    customer_address: Optional[str] = None

    address_display: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    company_contact_person: Optional[str] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    auto_repeat: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: Optional[bool] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    order_lost_reason: Optional[str] = None

    utm_source: Optional[str] = None

    utm_medium: Optional[str] = None

    utm_campaign: Optional[str] = None

    utm_content: Optional[str] = None

    status: Optional[QuotationStatus] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    title: Optional[str] = None

    opportunity: Optional[str] = None

    enq_det: Optional[str] = None

    supplier_quotation_id: Optional[uuid.UUID] = None

    items: Optional[list[QuotationItemCreate]] = None





class QuotationRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[QuotationNamingSeries] = None

    quotation_to: str

    party_name: Optional[str] = None

    customer_name: Optional[str] = None

    transaction_date: Optional[dt.date] = None

    valid_till: Optional[dt.date] = None

    order_type: Optional[QuotationOrderType] = None

    company: str

    has_unit_price_items: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    currency: str

    conversion_rate: Optional[Decimal] = None

    selling_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: str

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    scan_barcode: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

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

    rounded_total: Optional[Decimal] = None

    rounding_adjustment: Optional[Decimal] = None

    disable_rounded_total: Optional[bool] = None

    base_grand_total: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    base_rounded_total: Optional[Decimal] = None

    base_rounding_adjustment: Optional[Decimal] = None

    apply_discount_on: Optional[QuotationApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    coupon_code_id: Optional[uuid.UUID] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    referral_sales_partner: Optional[str] = None

    other_charges_calculation: Optional[str] = None

    customer_address: Optional[str] = None

    address_display: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    company_contact_person: Optional[str] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    auto_repeat: Optional[str] = None

    letter_head: Optional[str] = None

    group_same_items: Optional[bool] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    order_lost_reason: Optional[str] = None

    utm_source: Optional[str] = None

    utm_medium: Optional[str] = None

    utm_campaign: Optional[str] = None

    utm_content: Optional[str] = None

    status: Optional[QuotationStatus] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    title: Optional[str] = None

    opportunity: Optional[str] = None

    enq_det: Optional[str] = None

    supplier_quotation_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[QuotationItemRead] = []





QuotationListResponse = Page[QuotationRead]

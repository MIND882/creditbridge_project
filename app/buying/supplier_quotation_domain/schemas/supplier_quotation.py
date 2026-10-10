"""Pydantic v2 schemas for SupplierQuotation."""





from __future__ import annotations

from app.buying.supplier_quotation_domain.models.supplier_quotation import (

    SupplierQuotationNamingSeries,

    SupplierQuotationApplyDiscountOn,

    SupplierQuotationStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.buying.supplier_quotation_item_domain.schemas.supplier_quotation_item import (

    SupplierQuotationItemCreate,

    SupplierQuotationItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierQuotationCreate",

    "SupplierQuotationUpdate",

    "SupplierQuotationRead",

    "SupplierQuotationListResponse",

]





class SupplierQuotationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    title: Optional[str] = None

    naming_series: SupplierQuotationNamingSeries

    supplier_id: uuid.UUID

    supplier_name: Optional[str] = None

    transaction_date: dt.date

    amended_from_id: Optional[uuid.UUID] = None

    company: str

    supplier_address: Optional[str] = None

    contact_person: Optional[str] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    currency: str

    conversion_rate: Decimal

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    tax_category_id: Optional[uuid.UUID] = None

    shipping_rule_id: Optional[uuid.UUID] = None

    taxes_and_charges_id: Optional[uuid.UUID] = None

    other_charges_calculation: Optional[str] = None

    base_taxes_and_charges_added: Optional[Decimal] = None

    base_taxes_and_charges_deducted: Optional[Decimal] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    taxes_and_charges_added: Optional[Decimal] = None

    taxes_and_charges_deducted: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[SupplierQuotationApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_grand_total: Optional[Decimal] = None

    base_rounding_adjustment: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    base_rounded_total: Optional[Decimal] = None

    grand_total: Optional[Decimal] = None

    rounding_adjustment: Optional[Decimal] = None

    rounded_total: Optional[Decimal] = None

    in_words: Optional[str] = None

    disable_rounded_total: Optional[bool] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    select_print_heading: Optional[str] = None

    group_same_items: Optional[bool] = None

    letter_head: Optional[str] = None

    language: Optional[str] = None

    auto_repeat: Optional[str] = None

    status: SupplierQuotationStatus

    is_subcontracted: Optional[bool] = None

    opportunity: Optional[str] = None

    valid_till: Optional[dt.date] = None

    quotation_number: Optional[str] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    has_unit_price_items: Optional[bool] = None

    items: list[SupplierQuotationItemCreate] = []





class SupplierQuotationCreate(SupplierQuotationBase):

    pass





class SupplierQuotationUpdate(InputSchema):

    """A partial update."""



    title: Optional[str] = None

    naming_series: Optional[SupplierQuotationNamingSeries] = None

    supplier_id: Optional[uuid.UUID] = None

    supplier_name: Optional[str] = None

    transaction_date: Optional[dt.date] = None

    amended_from_id: Optional[uuid.UUID] = None

    company: Optional[str] = None

    supplier_address: Optional[str] = None

    contact_person: Optional[str] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    tax_category_id: Optional[uuid.UUID] = None

    shipping_rule_id: Optional[uuid.UUID] = None

    taxes_and_charges_id: Optional[uuid.UUID] = None

    other_charges_calculation: Optional[str] = None

    base_taxes_and_charges_added: Optional[Decimal] = None

    base_taxes_and_charges_deducted: Optional[Decimal] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    taxes_and_charges_added: Optional[Decimal] = None

    taxes_and_charges_deducted: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[SupplierQuotationApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_grand_total: Optional[Decimal] = None

    base_rounding_adjustment: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    base_rounded_total: Optional[Decimal] = None

    grand_total: Optional[Decimal] = None

    rounding_adjustment: Optional[Decimal] = None

    rounded_total: Optional[Decimal] = None

    in_words: Optional[str] = None

    disable_rounded_total: Optional[bool] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    select_print_heading: Optional[str] = None

    group_same_items: Optional[bool] = None

    letter_head: Optional[str] = None

    language: Optional[str] = None

    auto_repeat: Optional[str] = None

    status: Optional[SupplierQuotationStatus] = None

    is_subcontracted: Optional[bool] = None

    opportunity: Optional[str] = None

    valid_till: Optional[dt.date] = None

    quotation_number: Optional[str] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    has_unit_price_items: Optional[bool] = None

    items: Optional[list[SupplierQuotationItemCreate]] = None





class SupplierQuotationRead(ReadSchema):

    id: uuid.UUID

    name: str

    title: Optional[str] = None

    naming_series: Optional[SupplierQuotationNamingSeries] = None

    supplier_id: Optional[uuid.UUID] = None

    supplier_name: Optional[str] = None

    transaction_date: Optional[dt.date] = None

    amended_from_id: Optional[uuid.UUID] = None

    company: str

    supplier_address: Optional[str] = None

    contact_person: Optional[str] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    currency: str

    conversion_rate: Optional[Decimal] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    tax_category_id: Optional[uuid.UUID] = None

    shipping_rule_id: Optional[uuid.UUID] = None

    taxes_and_charges_id: Optional[uuid.UUID] = None

    other_charges_calculation: Optional[str] = None

    base_taxes_and_charges_added: Optional[Decimal] = None

    base_taxes_and_charges_deducted: Optional[Decimal] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    taxes_and_charges_added: Optional[Decimal] = None

    taxes_and_charges_deducted: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[SupplierQuotationApplyDiscountOn] = None

    base_discount_amount: Optional[Decimal] = None

    additional_discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_grand_total: Optional[Decimal] = None

    base_rounding_adjustment: Optional[Decimal] = None

    base_in_words: Optional[str] = None

    base_rounded_total: Optional[Decimal] = None

    grand_total: Optional[Decimal] = None

    rounding_adjustment: Optional[Decimal] = None

    rounded_total: Optional[Decimal] = None

    in_words: Optional[str] = None

    disable_rounded_total: Optional[bool] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    select_print_heading: Optional[str] = None

    group_same_items: Optional[bool] = None

    letter_head: Optional[str] = None

    language: Optional[str] = None

    auto_repeat: Optional[str] = None

    status: Optional[SupplierQuotationStatus] = None

    is_subcontracted: Optional[bool] = None

    opportunity: Optional[str] = None

    valid_till: Optional[dt.date] = None

    quotation_number: Optional[str] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    has_unit_price_items: Optional[bool] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[SupplierQuotationItemRead] = []





SupplierQuotationListResponse = Page[SupplierQuotationRead]

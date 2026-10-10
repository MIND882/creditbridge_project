"""Pydantic v2 schemas for DeliveryNote."""





from __future__ import annotations

from app.stock.delivery_note_domain.models.delivery_note import (

    DeliveryNoteNamingSeries,

    DeliveryNoteApplyDiscountOn,

    DeliveryNoteStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.delivery_note_item_domain.schemas.delivery_note_item import (

    DeliveryNoteItemCreate,

    DeliveryNoteItemRead,

)

from app.stock.packed_item_domain.schemas.packed_item import (

    PackedItemCreate,

    PackedItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "DeliveryNoteCreate",

    "DeliveryNoteUpdate",

    "DeliveryNoteRead",

    "DeliveryNoteListResponse",

]





class DeliveryNoteBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: DeliveryNoteNamingSeries

    customer: str

    customer_name: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    company: str

    posting_date: dt.date

    posting_time: dt.time

    set_posting_time: Optional[bool] = None

    is_return: Optional[bool] = None

    issue_credit_note: Optional[bool] = None

    return_against_id: Optional[uuid.UUID] = None

    po_no: Optional[str] = None

    po_date: Optional[dt.date] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    customer_address: Optional[str] = None

    tax_id: Optional[str] = None

    address_display: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    currency: str

    conversion_rate: Decimal

    selling_price_list_id: uuid.UUID

    price_list_currency: str

    plc_conversion_rate: Decimal

    ignore_pricing_rule: Optional[bool] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

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

    base_total_taxes_and_charges: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[DeliveryNoteApplyDiscountOn] = None

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

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    transporter: Optional[str] = None

    driver: Optional[str] = None

    lr_no: Optional[str] = None

    vehicle_no: Optional[str] = None

    transporter_name: Optional[str] = None

    driver_name: Optional[str] = None

    lr_date: Optional[dt.date] = None

    project: Optional[str] = None

    per_billed: Optional[Decimal] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    print_without_amount: Optional[bool] = None

    group_same_items: Optional[bool] = None

    status: DeliveryNoteStatus

    per_installed: Optional[Decimal] = None

    installation_status: Optional[str] = None

    excise_page: Optional[str] = None

    instructions: Optional[str] = None

    auto_repeat: Optional[str] = None

    sales_partner: Optional[str] = None

    commission_rate: Optional[Decimal] = None

    total_commission: Optional[Decimal] = None

    is_internal_customer: Optional[bool] = None

    inter_company_reference_id: Optional[uuid.UUID] = None

    per_returned: Optional[Decimal] = None

    set_target_warehouse_id: Optional[uuid.UUID] = None

    represents_company: Optional[str] = None

    disable_rounded_total: Optional[bool] = None

    dispatch_address_name: Optional[str] = None

    dispatch_address: Optional[str] = None

    amount_eligible_for_commission: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    delivery_trip_id: Optional[uuid.UUID] = None

    utm_medium: Optional[str] = None

    utm_content: Optional[str] = None

    utm_source: Optional[str] = None

    utm_campaign: Optional[str] = None

    company_contact_person: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    title: Optional[str] = None

    items: list[DeliveryNoteItemCreate] = []

    packed_items: list[PackedItemCreate] = []





class DeliveryNoteCreate(DeliveryNoteBase):

    pass





class DeliveryNoteUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[DeliveryNoteNamingSeries] = None

    customer: Optional[str] = None

    customer_name: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    company: Optional[str] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    is_return: Optional[bool] = None

    issue_credit_note: Optional[bool] = None

    return_against_id: Optional[uuid.UUID] = None

    po_no: Optional[str] = None

    po_date: Optional[dt.date] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    customer_address: Optional[str] = None

    tax_id: Optional[str] = None

    address_display: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    selling_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

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

    base_total_taxes_and_charges: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[DeliveryNoteApplyDiscountOn] = None

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

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    transporter: Optional[str] = None

    driver: Optional[str] = None

    lr_no: Optional[str] = None

    vehicle_no: Optional[str] = None

    transporter_name: Optional[str] = None

    driver_name: Optional[str] = None

    lr_date: Optional[dt.date] = None

    project: Optional[str] = None

    per_billed: Optional[Decimal] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    print_without_amount: Optional[bool] = None

    group_same_items: Optional[bool] = None

    status: Optional[DeliveryNoteStatus] = None

    per_installed: Optional[Decimal] = None

    installation_status: Optional[str] = None

    excise_page: Optional[str] = None

    instructions: Optional[str] = None

    auto_repeat: Optional[str] = None

    sales_partner: Optional[str] = None

    commission_rate: Optional[Decimal] = None

    total_commission: Optional[Decimal] = None

    is_internal_customer: Optional[bool] = None

    inter_company_reference_id: Optional[uuid.UUID] = None

    per_returned: Optional[Decimal] = None

    set_target_warehouse_id: Optional[uuid.UUID] = None

    represents_company: Optional[str] = None

    disable_rounded_total: Optional[bool] = None

    dispatch_address_name: Optional[str] = None

    dispatch_address: Optional[str] = None

    amount_eligible_for_commission: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    delivery_trip_id: Optional[uuid.UUID] = None

    utm_medium: Optional[str] = None

    utm_content: Optional[str] = None

    utm_source: Optional[str] = None

    utm_campaign: Optional[str] = None

    company_contact_person: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    title: Optional[str] = None

    items: Optional[list[DeliveryNoteItemCreate]] = None

    packed_items: Optional[list[PackedItemCreate]] = None





class DeliveryNoteRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[DeliveryNoteNamingSeries] = None

    customer: str

    customer_name: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    company: str

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    is_return: Optional[bool] = None

    issue_credit_note: Optional[bool] = None

    return_against_id: Optional[uuid.UUID] = None

    po_no: Optional[str] = None

    po_date: Optional[dt.date] = None

    shipping_address_name: Optional[str] = None

    shipping_address: Optional[str] = None

    contact_person: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    customer_address: Optional[str] = None

    tax_id: Optional[str] = None

    address_display: Optional[str] = None

    company_address: Optional[str] = None

    company_address_display: Optional[str] = None

    currency: str

    conversion_rate: Optional[Decimal] = None

    selling_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: str

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

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

    base_total_taxes_and_charges: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[DeliveryNoteApplyDiscountOn] = None

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

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    transporter: Optional[str] = None

    driver: Optional[str] = None

    lr_no: Optional[str] = None

    vehicle_no: Optional[str] = None

    transporter_name: Optional[str] = None

    driver_name: Optional[str] = None

    lr_date: Optional[dt.date] = None

    project: Optional[str] = None

    per_billed: Optional[Decimal] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    print_without_amount: Optional[bool] = None

    group_same_items: Optional[bool] = None

    status: Optional[DeliveryNoteStatus] = None

    per_installed: Optional[Decimal] = None

    installation_status: Optional[str] = None

    excise_page: Optional[str] = None

    instructions: Optional[str] = None

    auto_repeat: Optional[str] = None

    sales_partner: Optional[str] = None

    commission_rate: Optional[Decimal] = None

    total_commission: Optional[Decimal] = None

    is_internal_customer: Optional[bool] = None

    inter_company_reference_id: Optional[uuid.UUID] = None

    per_returned: Optional[Decimal] = None

    set_target_warehouse_id: Optional[uuid.UUID] = None

    represents_company: Optional[str] = None

    disable_rounded_total: Optional[bool] = None

    dispatch_address_name: Optional[str] = None

    dispatch_address: Optional[str] = None

    amount_eligible_for_commission: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    delivery_trip_id: Optional[uuid.UUID] = None

    utm_medium: Optional[str] = None

    utm_content: Optional[str] = None

    utm_source: Optional[str] = None

    utm_campaign: Optional[str] = None

    company_contact_person: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    title: Optional[str] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[DeliveryNoteItemRead] = []

    packed_items: list[PackedItemRead] = []





DeliveryNoteListResponse = Page[DeliveryNoteRead]

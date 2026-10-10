"""Pydantic v2 schemas for PurchaseOrder."""





from __future__ import annotations

from app.buying.purchase_order_domain.models.purchase_order import (

    PurchaseOrderNamingSeries,

    PurchaseOrderApplyDiscountOn,

    PurchaseOrderStatus,

    PurchaseOrderAdvancePaymentStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.buying.purchase_order_item_domain.schemas.purchase_order_item import (

    PurchaseOrderItemCreate,

    PurchaseOrderItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PurchaseOrderCreate",

    "PurchaseOrderUpdate",

    "PurchaseOrderRead",

    "PurchaseOrderListResponse",

]





class PurchaseOrderBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    title: Optional[str] = None

    naming_series: PurchaseOrderNamingSeries

    supplier_id: uuid.UUID

    supplier_name: Optional[str] = None

    company: str

    transaction_date: dt.date

    schedule_date: Optional[dt.date] = None

    order_confirmation_no: Optional[str] = None

    order_confirmation_date: Optional[dt.date] = None

    amended_from_id: Optional[uuid.UUID] = None

    customer: Optional[str] = None

    customer_name: Optional[str] = None

    customer_contact_person: Optional[str] = None

    customer_contact_display: Optional[str] = None

    customer_contact_mobile: Optional[str] = None

    customer_contact_email: Optional[str] = None

    supplier_address: Optional[str] = None

    contact_person: Optional[str] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    currency: str

    conversion_rate: Decimal

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    is_subcontracted: Optional[bool] = None

    supplier_warehouse_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    taxes_and_charges_id: Optional[uuid.UUID] = None

    shipping_rule_id: Optional[uuid.UUID] = None

    other_charges_calculation: Optional[str] = None

    base_taxes_and_charges_added: Optional[Decimal] = None

    base_taxes_and_charges_deducted: Optional[Decimal] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    taxes_and_charges_added: Optional[Decimal] = None

    taxes_and_charges_deducted: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[PurchaseOrderApplyDiscountOn] = None

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

    disable_rounded_total: Optional[bool] = None

    in_words: Optional[str] = None

    advance_paid: Optional[Decimal] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    status: PurchaseOrderStatus

    ref_sq_id: Optional[uuid.UUID] = None

    party_account_currency: Optional[str] = None

    inter_company_order_reference: Optional[str] = None

    per_received: Optional[Decimal] = None

    per_billed: Optional[Decimal] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    group_same_items: Optional[bool] = None

    language: Optional[str] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    set_reserve_warehouse_id: Optional[uuid.UUID] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    is_internal_supplier: Optional[bool] = None

    represents_company: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    set_from_warehouse_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    advance_payment_status: Optional[PurchaseOrderAdvancePaymentStatus] = None

    has_unit_price_items: Optional[bool] = None

    dispatch_address: Optional[str] = None

    dispatch_address_display: Optional[str] = None

    supplier_group: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    mps: Optional[str] = None

    transaction_time: Optional[dt.time] = None

    items: list[PurchaseOrderItemCreate] = []





class PurchaseOrderCreate(PurchaseOrderBase):

    pass





class PurchaseOrderUpdate(InputSchema):

    """A partial update."""



    title: Optional[str] = None

    naming_series: Optional[PurchaseOrderNamingSeries] = None

    supplier_id: Optional[uuid.UUID] = None

    supplier_name: Optional[str] = None

    company: Optional[str] = None

    transaction_date: Optional[dt.date] = None

    schedule_date: Optional[dt.date] = None

    order_confirmation_no: Optional[str] = None

    order_confirmation_date: Optional[dt.date] = None

    amended_from_id: Optional[uuid.UUID] = None

    customer: Optional[str] = None

    customer_name: Optional[str] = None

    customer_contact_person: Optional[str] = None

    customer_contact_display: Optional[str] = None

    customer_contact_mobile: Optional[str] = None

    customer_contact_email: Optional[str] = None

    supplier_address: Optional[str] = None

    contact_person: Optional[str] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    is_subcontracted: Optional[bool] = None

    supplier_warehouse_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    taxes_and_charges_id: Optional[uuid.UUID] = None

    shipping_rule_id: Optional[uuid.UUID] = None

    other_charges_calculation: Optional[str] = None

    base_taxes_and_charges_added: Optional[Decimal] = None

    base_taxes_and_charges_deducted: Optional[Decimal] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    taxes_and_charges_added: Optional[Decimal] = None

    taxes_and_charges_deducted: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[PurchaseOrderApplyDiscountOn] = None

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

    disable_rounded_total: Optional[bool] = None

    in_words: Optional[str] = None

    advance_paid: Optional[Decimal] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    status: Optional[PurchaseOrderStatus] = None

    ref_sq_id: Optional[uuid.UUID] = None

    party_account_currency: Optional[str] = None

    inter_company_order_reference: Optional[str] = None

    per_received: Optional[Decimal] = None

    per_billed: Optional[Decimal] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    group_same_items: Optional[bool] = None

    language: Optional[str] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    set_reserve_warehouse_id: Optional[uuid.UUID] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    is_internal_supplier: Optional[bool] = None

    represents_company: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    set_from_warehouse_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    advance_payment_status: Optional[PurchaseOrderAdvancePaymentStatus] = None

    has_unit_price_items: Optional[bool] = None

    dispatch_address: Optional[str] = None

    dispatch_address_display: Optional[str] = None

    supplier_group: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    mps: Optional[str] = None

    transaction_time: Optional[dt.time] = None

    items: Optional[list[PurchaseOrderItemCreate]] = None





class PurchaseOrderRead(ReadSchema):

    id: uuid.UUID

    name: str

    title: Optional[str] = None

    naming_series: Optional[PurchaseOrderNamingSeries] = None

    supplier_id: Optional[uuid.UUID] = None

    supplier_name: Optional[str] = None

    company: str

    transaction_date: Optional[dt.date] = None

    schedule_date: Optional[dt.date] = None

    order_confirmation_no: Optional[str] = None

    order_confirmation_date: Optional[dt.date] = None

    amended_from_id: Optional[uuid.UUID] = None

    customer: Optional[str] = None

    customer_name: Optional[str] = None

    customer_contact_person: Optional[str] = None

    customer_contact_display: Optional[str] = None

    customer_contact_mobile: Optional[str] = None

    customer_contact_email: Optional[str] = None

    supplier_address: Optional[str] = None

    contact_person: Optional[str] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    currency: str

    conversion_rate: Optional[Decimal] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    ignore_pricing_rule: Optional[bool] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    is_subcontracted: Optional[bool] = None

    supplier_warehouse_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Optional[Decimal] = None

    total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_net_weight: Optional[Decimal] = None

    taxes_and_charges_id: Optional[uuid.UUID] = None

    shipping_rule_id: Optional[uuid.UUID] = None

    other_charges_calculation: Optional[str] = None

    base_taxes_and_charges_added: Optional[Decimal] = None

    base_taxes_and_charges_deducted: Optional[Decimal] = None

    base_total_taxes_and_charges: Optional[Decimal] = None

    taxes_and_charges_added: Optional[Decimal] = None

    taxes_and_charges_deducted: Optional[Decimal] = None

    total_taxes_and_charges: Optional[Decimal] = None

    apply_discount_on: Optional[PurchaseOrderApplyDiscountOn] = None

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

    disable_rounded_total: Optional[bool] = None

    in_words: Optional[str] = None

    advance_paid: Optional[Decimal] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    status: Optional[PurchaseOrderStatus] = None

    ref_sq_id: Optional[uuid.UUID] = None

    party_account_currency: Optional[str] = None

    inter_company_order_reference: Optional[str] = None

    per_received: Optional[Decimal] = None

    per_billed: Optional[Decimal] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    group_same_items: Optional[bool] = None

    language: Optional[str] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    auto_repeat: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    set_reserve_warehouse_id: Optional[uuid.UUID] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    is_internal_supplier: Optional[bool] = None

    represents_company: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    set_from_warehouse_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    advance_payment_status: Optional[PurchaseOrderAdvancePaymentStatus] = None

    has_unit_price_items: Optional[bool] = None

    dispatch_address: Optional[str] = None

    dispatch_address_display: Optional[str] = None

    supplier_group: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    mps: Optional[str] = None

    transaction_time: Optional[dt.time] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[PurchaseOrderItemRead] = []





PurchaseOrderListResponse = Page[PurchaseOrderRead]

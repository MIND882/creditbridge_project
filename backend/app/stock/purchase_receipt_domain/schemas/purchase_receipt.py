"""Pydantic v2 schemas for PurchaseReceipt."""





from __future__ import annotations

from app.stock.purchase_receipt_domain.models.purchase_receipt import (

    PurchaseReceiptNamingSeries,

    PurchaseReceiptApplyDiscountOn,

    PurchaseReceiptStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.purchase_receipt_item_domain.schemas.purchase_receipt_item import (

    PurchaseReceiptItemCreate,

    PurchaseReceiptItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PurchaseReceiptCreate",

    "PurchaseReceiptUpdate",

    "PurchaseReceiptRead",

    "PurchaseReceiptListResponse",

]





class PurchaseReceiptBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    title: Optional[str] = None

    naming_series: PurchaseReceiptNamingSeries

    supplier: str

    supplier_name: Optional[str] = None

    supplier_delivery_note: Optional[str] = None

    posting_date: dt.date

    posting_time: dt.time

    set_posting_time: Optional[bool] = None

    company: str

    is_return: Optional[bool] = None

    return_against_id: Optional[uuid.UUID] = None

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

    rejected_warehouse_id: Optional[uuid.UUID] = None

    is_subcontracted: Optional[bool] = None

    supplier_warehouse_id: Optional[uuid.UUID] = None

    total_qty: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_net_total: Decimal

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

    apply_discount_on: Optional[PurchaseReceiptApplyDiscountOn] = None

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

    status: PurchaseReceiptStatus

    amended_from_id: Optional[uuid.UUID] = None

    range: Optional[str] = None

    project: Optional[str] = None

    per_billed: Optional[Decimal] = None

    auto_repeat: Optional[str] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    group_same_items: Optional[bool] = None

    instructions: Optional[str] = None

    remarks: Optional[str] = None

    transporter_name: Optional[str] = None

    lr_no: Optional[str] = None

    lr_date: Optional[dt.date] = None

    is_internal_supplier: Optional[bool] = None

    inter_company_reference_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    apply_putaway_rule: Optional[bool] = None

    per_returned: Optional[Decimal] = None

    set_from_warehouse_id: Optional[uuid.UUID] = None

    represents_company: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    subcontracting_receipt: Optional[str] = None

    dispatch_address: Optional[str] = None

    dispatch_address_display: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    items: list[PurchaseReceiptItemCreate] = []





class PurchaseReceiptCreate(PurchaseReceiptBase):

    pass





class PurchaseReceiptUpdate(InputSchema):

    """A partial update."""



    title: Optional[str] = None

    naming_series: Optional[PurchaseReceiptNamingSeries] = None

    supplier: Optional[str] = None

    supplier_name: Optional[str] = None

    supplier_delivery_note: Optional[str] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    company: Optional[str] = None

    is_return: Optional[bool] = None

    return_against_id: Optional[uuid.UUID] = None

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

    rejected_warehouse_id: Optional[uuid.UUID] = None

    is_subcontracted: Optional[bool] = None

    supplier_warehouse_id: Optional[uuid.UUID] = None

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

    apply_discount_on: Optional[PurchaseReceiptApplyDiscountOn] = None

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

    status: Optional[PurchaseReceiptStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    range: Optional[str] = None

    project: Optional[str] = None

    per_billed: Optional[Decimal] = None

    auto_repeat: Optional[str] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    group_same_items: Optional[bool] = None

    instructions: Optional[str] = None

    remarks: Optional[str] = None

    transporter_name: Optional[str] = None

    lr_no: Optional[str] = None

    lr_date: Optional[dt.date] = None

    is_internal_supplier: Optional[bool] = None

    inter_company_reference_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    apply_putaway_rule: Optional[bool] = None

    per_returned: Optional[Decimal] = None

    set_from_warehouse_id: Optional[uuid.UUID] = None

    represents_company: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    subcontracting_receipt: Optional[str] = None

    dispatch_address: Optional[str] = None

    dispatch_address_display: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    items: Optional[list[PurchaseReceiptItemCreate]] = None





class PurchaseReceiptRead(ReadSchema):

    id: uuid.UUID

    name: str

    title: Optional[str] = None

    naming_series: Optional[PurchaseReceiptNamingSeries] = None

    supplier: str

    supplier_name: Optional[str] = None

    supplier_delivery_note: Optional[str] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    company: str

    is_return: Optional[bool] = None

    return_against_id: Optional[uuid.UUID] = None

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

    rejected_warehouse_id: Optional[uuid.UUID] = None

    is_subcontracted: Optional[bool] = None

    supplier_warehouse_id: Optional[uuid.UUID] = None

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

    apply_discount_on: Optional[PurchaseReceiptApplyDiscountOn] = None

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

    status: Optional[PurchaseReceiptStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    range: Optional[str] = None

    project: Optional[str] = None

    per_billed: Optional[Decimal] = None

    auto_repeat: Optional[str] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    language: Optional[str] = None

    group_same_items: Optional[bool] = None

    instructions: Optional[str] = None

    remarks: Optional[str] = None

    transporter_name: Optional[str] = None

    lr_no: Optional[str] = None

    lr_date: Optional[dt.date] = None

    is_internal_supplier: Optional[bool] = None

    inter_company_reference_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    apply_putaway_rule: Optional[bool] = None

    per_returned: Optional[Decimal] = None

    set_from_warehouse_id: Optional[uuid.UUID] = None

    represents_company: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    subcontracting_receipt: Optional[str] = None

    dispatch_address: Optional[str] = None

    dispatch_address_display: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[PurchaseReceiptItemRead] = []





PurchaseReceiptListResponse = Page[PurchaseReceiptRead]

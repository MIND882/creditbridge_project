"""Pydantic v2 schemas for PurchaseInvoiceItem."""





from __future__ import annotations

from app.accounts.purchase_invoice_item_domain.models.purchase_invoice_item import (

    PurchaseInvoiceItemMarginType,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PurchaseInvoiceItemCreate",

    "PurchaseInvoiceItemRead",

    "PurchaseInvoiceItemListResponse",

]





class PurchaseInvoiceItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code: Optional[str] = None

    item_name: str

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    received_qty: Optional[Decimal] = None

    qty: Optional[Decimal] = None

    rejected_qty: Optional[Decimal] = None

    stock_uom: Optional[str] = None

    uom: str

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    base_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    pricing_rules: Optional[str] = None

    is_free_item: Optional[bool] = None

    net_rate: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    base_net_rate: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom: Optional[str] = None

    warehouse: Optional[str] = None

    rejected_warehouse: Optional[str] = None

    quality_inspection: Optional[str] = None

    batch_no: Optional[str] = None

    serial_no: Optional[str] = None

    rejected_serial_no: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    deferred_expense_account_id: Optional[uuid.UUID] = None

    service_stop_date: Optional[dt.date] = None

    enable_deferred_expense: Optional[bool] = None

    service_start_date: Optional[dt.date] = None

    service_end_date: Optional[dt.date] = None

    allow_zero_valuation_rate: Optional[bool] = None

    brand: Optional[str] = None

    item_group: Optional[str] = None

    item_tax_rate: Optional[str] = None

    item_tax_amount: Optional[Decimal] = None

    purchase_order: Optional[str] = None

    include_exploded_items: Optional[bool] = None

    is_fixed_asset: Optional[bool] = None

    asset_location: Optional[str] = None

    po_detail: Optional[str] = None

    purchase_receipt: Optional[str] = None

    page_break: Optional[bool] = None

    pr_detail: Optional[str] = None

    valuation_rate: Optional[Decimal] = None

    rm_supp_cost: Optional[Decimal] = None

    landed_cost_voucher_amount: Optional[Decimal] = None

    manufacturer: Optional[str] = None

    manufacturer_part_no: Optional[str] = None

    asset_category: Optional[str] = None

    from_warehouse: Optional[str] = None

    purchase_invoice_item: Optional[str] = None

    stock_uom_rate: Optional[Decimal] = None

    sales_invoice_item: Optional[str] = None

    margin_type: Optional[PurchaseInvoiceItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    product_bundle: Optional[str] = None

    apply_tds: Optional[bool] = None

    serial_and_batch_bundle: Optional[str] = None

    rejected_serial_and_batch_bundle: Optional[str] = None

    wip_composite_asset: Optional[str] = None

    use_serial_batch_fields: Optional[bool] = None

    material_request: Optional[str] = None

    material_request_item: Optional[str] = None

    sales_incoming_rate: Optional[Decimal] = None

    distributed_discount_amount: Optional[Decimal] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    delivered_by_supplier: Optional[bool] = None





class PurchaseInvoiceItemCreate(PurchaseInvoiceItemBase):

    """Accepted only nested inside the parent payload."""

    pass





class PurchaseInvoiceItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    item_code: Optional[str] = None

    item_name: str

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    received_qty: Optional[Decimal] = None

    qty: Decimal

    rejected_qty: Optional[Decimal] = None

    stock_uom: Optional[str] = None

    uom: str

    conversion_factor: Decimal

    stock_qty: Decimal

    price_list_rate: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    rate: Decimal

    amount: Decimal

    base_rate: Decimal

    base_amount: Decimal

    pricing_rules: Optional[str] = None

    is_free_item: bool

    net_rate: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    base_net_rate: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom: Optional[str] = None

    warehouse: Optional[str] = None

    rejected_warehouse: Optional[str] = None

    quality_inspection: Optional[str] = None

    batch_no: Optional[str] = None

    serial_no: Optional[str] = None

    rejected_serial_no: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    deferred_expense_account_id: Optional[uuid.UUID] = None

    service_stop_date: Optional[dt.date] = None

    enable_deferred_expense: bool

    service_start_date: Optional[dt.date] = None

    service_end_date: Optional[dt.date] = None

    allow_zero_valuation_rate: bool

    brand: Optional[str] = None

    item_group: Optional[str] = None

    item_tax_rate: Optional[str] = None

    item_tax_amount: Optional[Decimal] = None

    purchase_order: Optional[str] = None

    include_exploded_items: bool

    is_fixed_asset: bool

    asset_location: Optional[str] = None

    po_detail: Optional[str] = None

    purchase_receipt: Optional[str] = None

    page_break: bool

    pr_detail: Optional[str] = None

    valuation_rate: Optional[Decimal] = None

    rm_supp_cost: Optional[Decimal] = None

    landed_cost_voucher_amount: Optional[Decimal] = None

    manufacturer: Optional[str] = None

    manufacturer_part_no: Optional[str] = None

    asset_category: Optional[str] = None

    from_warehouse: Optional[str] = None

    purchase_invoice_item: Optional[str] = None

    stock_uom_rate: Optional[Decimal] = None

    sales_invoice_item: Optional[str] = None

    margin_type: Optional[PurchaseInvoiceItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    product_bundle: Optional[str] = None

    apply_tds: bool

    serial_and_batch_bundle: Optional[str] = None

    rejected_serial_and_batch_bundle: Optional[str] = None

    wip_composite_asset: Optional[str] = None

    use_serial_batch_fields: bool

    material_request: Optional[str] = None

    material_request_item: Optional[str] = None

    sales_incoming_rate: Optional[Decimal] = None

    distributed_discount_amount: Optional[Decimal] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    delivered_by_supplier: bool





PurchaseInvoiceItemListResponse = Page[PurchaseInvoiceItemRead]

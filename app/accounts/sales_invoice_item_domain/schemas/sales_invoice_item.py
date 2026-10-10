"""Pydantic v2 schemas for SalesInvoiceItem."""





from __future__ import annotations

from app.accounts.sales_invoice_item_domain.models.sales_invoice_item import (

    SalesInvoiceItemMarginType,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesInvoiceItemCreate",

    "SalesInvoiceItemRead",

    "SalesInvoiceItemListResponse",

]





class SalesInvoiceItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    barcode: Optional[str] = None

    item_code: Optional[str] = None

    is_product_bundle: Optional[bool] = None

    product_bundle: Optional[str] = None

    item_name: str

    customer_item_code: Optional[str] = None

    description: Optional[str] = None

    image_view: Optional[str] = None

    image: Optional[str] = None

    qty: Optional[Decimal] = None

    stock_uom: Optional[str] = None

    uom: str

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    margin_type: Optional[SalesInvoiceItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

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

    delivered_by_supplier: Optional[bool] = None

    income_account_id: uuid.UUID

    expense_account_id: Optional[uuid.UUID] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    cost_center_id: uuid.UUID

    deferred_revenue_account_id: Optional[uuid.UUID] = None

    service_stop_date: Optional[dt.date] = None

    enable_deferred_revenue: Optional[bool] = None

    service_start_date: Optional[dt.date] = None

    service_end_date: Optional[dt.date] = None

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom: Optional[str] = None

    warehouse: Optional[str] = None

    target_warehouse: Optional[str] = None

    quality_inspection: Optional[str] = None

    batch_no: Optional[str] = None

    allow_zero_valuation_rate: Optional[bool] = None

    serial_no: Optional[str] = None

    item_group: Optional[str] = None

    brand: Optional[str] = None

    item_tax_rate: Optional[str] = None

    actual_batch_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    sales_order: Optional[str] = None

    so_detail: Optional[str] = None

    delivery_note: Optional[str] = None

    dn_detail: Optional[str] = None

    delivered_qty: Optional[Decimal] = None

    is_fixed_asset: Optional[bool] = None

    asset: Optional[str] = None

    page_break: Optional[bool] = None

    finance_book_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    sales_invoice_item: Optional[str] = None

    incoming_rate: Optional[Decimal] = None

    stock_uom_rate: Optional[Decimal] = None

    discount_account_id: Optional[uuid.UUID] = None

    grant_commission: Optional[bool] = None

    purchase_order: Optional[str] = None

    purchase_order_item: Optional[str] = None

    has_item_scanned: Optional[bool] = None

    serial_and_batch_bundle: Optional[str] = None

    use_serial_batch_fields: Optional[bool] = None

    distributed_discount_amount: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    pos_invoice_item: Optional[str] = None

    pos_invoice: Optional[str] = None

    scio_detail: Optional[str] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    apply_tds: Optional[bool] = None

    against_pick_list: Optional[str] = None

    pick_list_item: Optional[str] = None





class SalesInvoiceItemCreate(SalesInvoiceItemBase):

    """Accepted only nested inside the parent payload."""

    pass





class SalesInvoiceItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    barcode: Optional[str] = None

    item_code: Optional[str] = None

    is_product_bundle: bool

    product_bundle: Optional[str] = None

    item_name: str

    customer_item_code: Optional[str] = None

    description: Optional[str] = None

    image_view: Optional[str] = None

    image: Optional[str] = None

    qty: Optional[Decimal] = None

    stock_uom: Optional[str] = None

    uom: str

    conversion_factor: Decimal

    stock_qty: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    margin_type: Optional[SalesInvoiceItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

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

    delivered_by_supplier: bool

    income_account_id: uuid.UUID

    expense_account_id: Optional[uuid.UUID] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    cost_center_id: uuid.UUID

    deferred_revenue_account_id: Optional[uuid.UUID] = None

    service_stop_date: Optional[dt.date] = None

    enable_deferred_revenue: bool

    service_start_date: Optional[dt.date] = None

    service_end_date: Optional[dt.date] = None

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom: Optional[str] = None

    warehouse: Optional[str] = None

    target_warehouse: Optional[str] = None

    quality_inspection: Optional[str] = None

    batch_no: Optional[str] = None

    allow_zero_valuation_rate: bool

    serial_no: Optional[str] = None

    item_group: Optional[str] = None

    brand: Optional[str] = None

    item_tax_rate: Optional[str] = None

    actual_batch_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    sales_order: Optional[str] = None

    so_detail: Optional[str] = None

    delivery_note: Optional[str] = None

    dn_detail: Optional[str] = None

    delivered_qty: Optional[Decimal] = None

    is_fixed_asset: bool

    asset: Optional[str] = None

    page_break: bool

    finance_book_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    sales_invoice_item: Optional[str] = None

    incoming_rate: Optional[Decimal] = None

    stock_uom_rate: Optional[Decimal] = None

    discount_account_id: Optional[uuid.UUID] = None

    grant_commission: bool

    purchase_order: Optional[str] = None

    purchase_order_item: Optional[str] = None

    has_item_scanned: bool

    serial_and_batch_bundle: Optional[str] = None

    use_serial_batch_fields: bool

    distributed_discount_amount: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    pos_invoice_item: Optional[str] = None

    pos_invoice: Optional[str] = None

    scio_detail: Optional[str] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    apply_tds: bool

    against_pick_list: Optional[str] = None

    pick_list_item: Optional[str] = None





SalesInvoiceItemListResponse = Page[SalesInvoiceItemRead]

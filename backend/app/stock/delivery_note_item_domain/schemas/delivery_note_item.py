"""Pydantic v2 schemas for DeliveryNoteItem."""





from __future__ import annotations

from app.stock.delivery_note_item_domain.models.delivery_note_item import (

    DeliveryNoteItemMarginType,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "DeliveryNoteItemCreate",

    "DeliveryNoteItemRead",

    "DeliveryNoteItemListResponse",

]





class DeliveryNoteItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    barcode: Optional[str] = None

    item_code_id: uuid.UUID

    is_product_bundle: Optional[bool] = None

    product_bundle: Optional[str] = None

    item_name: str

    customer_item_code: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Decimal

    stock_uom_id: uuid.UUID

    uom_id: uuid.UUID

    conversion_factor: Decimal

    stock_qty: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    margin_type: Optional[DeliveryNoteItemMarginType] = None

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

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    target_warehouse_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    actual_qty: Optional[Decimal] = None

    actual_batch_qty: Optional[Decimal] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    item_tax_rate: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    allow_zero_valuation_rate: Optional[bool] = None

    against_sales_order: Optional[str] = None

    against_sales_invoice_id: Optional[uuid.UUID] = None

    so_detail: Optional[str] = None

    si_detail: Optional[str] = None

    installed_qty: Optional[Decimal] = None

    billed_amt: Optional[Decimal] = None

    page_break: Optional[bool] = None

    project: Optional[str] = None

    dn_detail: Optional[str] = None

    returned_qty: Optional[Decimal] = None

    incoming_rate: Optional[Decimal] = None

    stock_uom_rate: Optional[Decimal] = None

    grant_commission: Optional[bool] = None

    pick_list_item: Optional[str] = None

    purchase_order: Optional[str] = None

    purchase_order_item: Optional[str] = None

    has_item_scanned: Optional[bool] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    received_qty: Optional[Decimal] = None

    packed_qty: Optional[Decimal] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    distributed_discount_amount: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    against_pick_list_id: Optional[uuid.UUID] = None





class DeliveryNoteItemCreate(DeliveryNoteItemBase):

    pass





class DeliveryNoteItemUpdate(InputSchema):

    """A partial update."""



    barcode: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    is_product_bundle: Optional[bool] = None

    product_bundle: Optional[str] = None

    item_name: Optional[str] = None

    customer_item_code: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    margin_type: Optional[DeliveryNoteItemMarginType] = None

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

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    target_warehouse_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    actual_qty: Optional[Decimal] = None

    actual_batch_qty: Optional[Decimal] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    item_tax_rate: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    allow_zero_valuation_rate: Optional[bool] = None

    against_sales_order: Optional[str] = None

    against_sales_invoice_id: Optional[uuid.UUID] = None

    so_detail: Optional[str] = None

    si_detail: Optional[str] = None

    installed_qty: Optional[Decimal] = None

    billed_amt: Optional[Decimal] = None

    page_break: Optional[bool] = None

    project: Optional[str] = None

    dn_detail: Optional[str] = None

    returned_qty: Optional[Decimal] = None

    incoming_rate: Optional[Decimal] = None

    stock_uom_rate: Optional[Decimal] = None

    grant_commission: Optional[bool] = None

    pick_list_item: Optional[str] = None

    purchase_order: Optional[str] = None

    purchase_order_item: Optional[str] = None

    has_item_scanned: Optional[bool] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    received_qty: Optional[Decimal] = None

    packed_qty: Optional[Decimal] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    distributed_discount_amount: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    against_pick_list_id: Optional[uuid.UUID] = None





class DeliveryNoteItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    barcode: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    is_product_bundle: Optional[bool] = None

    product_bundle: Optional[str] = None

    item_name: str

    customer_item_code: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    margin_type: Optional[DeliveryNoteItemMarginType] = None

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

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    target_warehouse_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    actual_qty: Optional[Decimal] = None

    actual_batch_qty: Optional[Decimal] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    item_tax_rate: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    allow_zero_valuation_rate: Optional[bool] = None

    against_sales_order: Optional[str] = None

    against_sales_invoice_id: Optional[uuid.UUID] = None

    so_detail: Optional[str] = None

    si_detail: Optional[str] = None

    installed_qty: Optional[Decimal] = None

    billed_amt: Optional[Decimal] = None

    page_break: Optional[bool] = None

    project: Optional[str] = None

    dn_detail: Optional[str] = None

    returned_qty: Optional[Decimal] = None

    incoming_rate: Optional[Decimal] = None

    stock_uom_rate: Optional[Decimal] = None

    grant_commission: Optional[bool] = None

    pick_list_item: Optional[str] = None

    purchase_order: Optional[str] = None

    purchase_order_item: Optional[str] = None

    has_item_scanned: Optional[bool] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    received_qty: Optional[Decimal] = None

    packed_qty: Optional[Decimal] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    distributed_discount_amount: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    against_pick_list_id: Optional[uuid.UUID] = None





DeliveryNoteItemListResponse = Page[DeliveryNoteItemRead]

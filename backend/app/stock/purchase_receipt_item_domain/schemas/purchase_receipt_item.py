"""Pydantic v2 schemas for PurchaseReceiptItem."""





from __future__ import annotations

from app.stock.purchase_receipt_item_domain.models.purchase_receipt_item import (

    PurchaseReceiptItemMarginType,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PurchaseReceiptItemCreate",

    "PurchaseReceiptItemRead",

    "PurchaseReceiptItemListResponse",

]





class PurchaseReceiptItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    barcode: Optional[str] = None

    item_code_id: uuid.UUID

    supplier_part_no: Optional[str] = None

    item_name: str

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    received_qty: Decimal

    qty: Optional[Decimal] = None

    rejected_qty: Optional[Decimal] = None

    uom_id: uuid.UUID

    stock_uom_id: uuid.UUID

    conversion_factor: Decimal

    retain_sample: Optional[bool] = None

    sample_quantity: Optional[int] = None

    price_list_rate: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    base_rate: Decimal

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

    rejected_warehouse_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    is_fixed_asset: Optional[bool] = None

    purchase_order: Optional[str] = None

    schedule_date: Optional[dt.date] = None

    stock_qty: Optional[Decimal] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    purchase_order_item: Optional[str] = None

    allow_zero_valuation_rate: Optional[bool] = None

    billed_amt: Optional[Decimal] = None

    landed_cost_voucher_amount: Optional[Decimal] = None

    brand_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    rm_supp_cost: Optional[Decimal] = None

    item_tax_amount: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    item_tax_rate: Optional[str] = None

    page_break: Optional[bool] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    asset_location: Optional[str] = None

    asset_category: Optional[str] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    purchase_receipt_item: Optional[str] = None

    putaway_rule_id: Optional[uuid.UUID] = None

    returned_qty: Optional[Decimal] = None

    received_stock_qty: Optional[Decimal] = None

    stock_uom_rate: Optional[Decimal] = None

    delivery_note_item: Optional[str] = None

    margin_type: Optional[PurchaseReceiptItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    purchase_invoice_id: Optional[uuid.UUID] = None

    purchase_invoice_item: Optional[str] = None

    product_bundle: Optional[str] = None

    provisional_expense_account_id: Optional[uuid.UUID] = None

    has_item_scanned: Optional[bool] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    rejected_serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    rejected_serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    wip_composite_asset: Optional[str] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    subcontracting_receipt_item: Optional[str] = None

    use_serial_batch_fields: Optional[bool] = None

    return_qty_from_rejected_warehouse: Optional[bool] = None

    sales_incoming_rate: Optional[Decimal] = None

    distributed_discount_amount: Optional[Decimal] = None

    amount_difference_with_purchase_invoice: Optional[Decimal] = None





class PurchaseReceiptItemCreate(PurchaseReceiptItemBase):

    pass





class PurchaseReceiptItemUpdate(InputSchema):

    """A partial update."""



    barcode: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    supplier_part_no: Optional[str] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    received_qty: Optional[Decimal] = None

    qty: Optional[Decimal] = None

    rejected_qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    retain_sample: Optional[bool] = None

    sample_quantity: Optional[int] = None

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

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    rejected_warehouse_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    is_fixed_asset: Optional[bool] = None

    purchase_order: Optional[str] = None

    schedule_date: Optional[dt.date] = None

    stock_qty: Optional[Decimal] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    purchase_order_item: Optional[str] = None

    allow_zero_valuation_rate: Optional[bool] = None

    billed_amt: Optional[Decimal] = None

    landed_cost_voucher_amount: Optional[Decimal] = None

    brand_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    rm_supp_cost: Optional[Decimal] = None

    item_tax_amount: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    item_tax_rate: Optional[str] = None

    page_break: Optional[bool] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    asset_location: Optional[str] = None

    asset_category: Optional[str] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    purchase_receipt_item: Optional[str] = None

    putaway_rule_id: Optional[uuid.UUID] = None

    returned_qty: Optional[Decimal] = None

    received_stock_qty: Optional[Decimal] = None

    stock_uom_rate: Optional[Decimal] = None

    delivery_note_item: Optional[str] = None

    margin_type: Optional[PurchaseReceiptItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    purchase_invoice_id: Optional[uuid.UUID] = None

    purchase_invoice_item: Optional[str] = None

    product_bundle: Optional[str] = None

    provisional_expense_account_id: Optional[uuid.UUID] = None

    has_item_scanned: Optional[bool] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    rejected_serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    rejected_serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    wip_composite_asset: Optional[str] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    subcontracting_receipt_item: Optional[str] = None

    use_serial_batch_fields: Optional[bool] = None

    return_qty_from_rejected_warehouse: Optional[bool] = None

    sales_incoming_rate: Optional[Decimal] = None

    distributed_discount_amount: Optional[Decimal] = None

    amount_difference_with_purchase_invoice: Optional[Decimal] = None





class PurchaseReceiptItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    barcode: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    supplier_part_no: Optional[str] = None

    item_name: str

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    received_qty: Optional[Decimal] = None

    qty: Optional[Decimal] = None

    rejected_qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    retain_sample: Optional[bool] = None

    sample_quantity: Optional[int] = None

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

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    rejected_warehouse_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    is_fixed_asset: Optional[bool] = None

    purchase_order: Optional[str] = None

    schedule_date: Optional[dt.date] = None

    stock_qty: Optional[Decimal] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    purchase_order_item: Optional[str] = None

    allow_zero_valuation_rate: Optional[bool] = None

    billed_amt: Optional[Decimal] = None

    landed_cost_voucher_amount: Optional[Decimal] = None

    brand_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    rm_supp_cost: Optional[Decimal] = None

    item_tax_amount: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    item_tax_rate: Optional[str] = None

    page_break: Optional[bool] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    asset_location: Optional[str] = None

    asset_category: Optional[str] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    purchase_receipt_item: Optional[str] = None

    putaway_rule_id: Optional[uuid.UUID] = None

    returned_qty: Optional[Decimal] = None

    received_stock_qty: Optional[Decimal] = None

    stock_uom_rate: Optional[Decimal] = None

    delivery_note_item: Optional[str] = None

    margin_type: Optional[PurchaseReceiptItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    purchase_invoice_id: Optional[uuid.UUID] = None

    purchase_invoice_item: Optional[str] = None

    product_bundle: Optional[str] = None

    provisional_expense_account_id: Optional[uuid.UUID] = None

    has_item_scanned: Optional[bool] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    rejected_serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    rejected_serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    wip_composite_asset: Optional[str] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    subcontracting_receipt_item: Optional[str] = None

    use_serial_batch_fields: Optional[bool] = None

    return_qty_from_rejected_warehouse: Optional[bool] = None

    sales_incoming_rate: Optional[Decimal] = None

    distributed_discount_amount: Optional[Decimal] = None

    amount_difference_with_purchase_invoice: Optional[Decimal] = None





PurchaseReceiptItemListResponse = Page[PurchaseReceiptItemRead]

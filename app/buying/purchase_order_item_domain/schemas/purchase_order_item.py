"""Pydantic v2 schemas for PurchaseOrderItem."""





from __future__ import annotations

from app.buying.purchase_order_item_domain.models.purchase_order_item import (

    PurchaseOrderItemMarginType,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PurchaseOrderItemCreate",

    "PurchaseOrderItemRead",

    "PurchaseOrderItemListResponse",

]





class PurchaseOrderItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    supplier_part_no: Optional[str] = None

    item_name: str

    schedule_date: dt.date

    expected_delivery_date: Optional[dt.date] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Decimal

    stock_uom_id: uuid.UUID

    uom_id: uuid.UUID

    conversion_factor: Decimal

    price_list_rate: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    last_purchase_rate: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    base_rate: Decimal

    base_amount: Decimal

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

    project: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    supplier_quotation_id: Optional[uuid.UUID] = None

    supplier_quotation_item_id: Optional[uuid.UUID] = None

    delivered_by_supplier: Optional[bool] = None

    blanket_order: Optional[str] = None

    blanket_order_rate: Optional[Decimal] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    bom: Optional[str] = None

    stock_qty: Optional[Decimal] = None

    received_qty: Optional[Decimal] = None

    returned_qty: Optional[Decimal] = None

    billed_amt: Optional[Decimal] = None

    item_tax_rate: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    against_blanket_order: Optional[bool] = None

    is_fixed_asset: Optional[bool] = None

    stock_uom_rate: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    margin_type: Optional[PurchaseOrderItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    production_plan: Optional[str] = None

    production_plan_item: Optional[str] = None

    production_plan_sub_assembly_item: Optional[str] = None

    product_bundle: Optional[str] = None

    sales_order_packed_item: Optional[str] = None

    fg_item_id: Optional[uuid.UUID] = None

    fg_item_qty: Optional[Decimal] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    wip_composite_asset: Optional[str] = None

    job_card: Optional[str] = None

    distributed_discount_amount: Optional[Decimal] = None

    subcontracted_qty: Optional[Decimal] = None





class PurchaseOrderItemCreate(PurchaseOrderItemBase):

    pass





class PurchaseOrderItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    supplier_part_no: Optional[str] = None

    item_name: Optional[str] = None

    schedule_date: Optional[dt.date] = None

    expected_delivery_date: Optional[dt.date] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    last_purchase_rate: Optional[Decimal] = None

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

    project: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    supplier_quotation_id: Optional[uuid.UUID] = None

    supplier_quotation_item_id: Optional[uuid.UUID] = None

    delivered_by_supplier: Optional[bool] = None

    blanket_order: Optional[str] = None

    blanket_order_rate: Optional[Decimal] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    bom: Optional[str] = None

    stock_qty: Optional[Decimal] = None

    received_qty: Optional[Decimal] = None

    returned_qty: Optional[Decimal] = None

    billed_amt: Optional[Decimal] = None

    item_tax_rate: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    against_blanket_order: Optional[bool] = None

    is_fixed_asset: Optional[bool] = None

    stock_uom_rate: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    margin_type: Optional[PurchaseOrderItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    production_plan: Optional[str] = None

    production_plan_item: Optional[str] = None

    production_plan_sub_assembly_item: Optional[str] = None

    product_bundle: Optional[str] = None

    sales_order_packed_item: Optional[str] = None

    fg_item_id: Optional[uuid.UUID] = None

    fg_item_qty: Optional[Decimal] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    wip_composite_asset: Optional[str] = None

    job_card: Optional[str] = None

    distributed_discount_amount: Optional[Decimal] = None

    subcontracted_qty: Optional[Decimal] = None





class PurchaseOrderItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    supplier_part_no: Optional[str] = None

    item_name: str

    schedule_date: Optional[dt.date] = None

    expected_delivery_date: Optional[dt.date] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    last_purchase_rate: Optional[Decimal] = None

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

    project: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    supplier_quotation_id: Optional[uuid.UUID] = None

    supplier_quotation_item_id: Optional[uuid.UUID] = None

    delivered_by_supplier: Optional[bool] = None

    blanket_order: Optional[str] = None

    blanket_order_rate: Optional[Decimal] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    bom: Optional[str] = None

    stock_qty: Optional[Decimal] = None

    received_qty: Optional[Decimal] = None

    returned_qty: Optional[Decimal] = None

    billed_amt: Optional[Decimal] = None

    item_tax_rate: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    against_blanket_order: Optional[bool] = None

    is_fixed_asset: Optional[bool] = None

    stock_uom_rate: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    margin_type: Optional[PurchaseOrderItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    production_plan: Optional[str] = None

    production_plan_item: Optional[str] = None

    production_plan_sub_assembly_item: Optional[str] = None

    product_bundle: Optional[str] = None

    sales_order_packed_item: Optional[str] = None

    fg_item_id: Optional[uuid.UUID] = None

    fg_item_qty: Optional[Decimal] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    wip_composite_asset: Optional[str] = None

    job_card: Optional[str] = None

    distributed_discount_amount: Optional[Decimal] = None

    subcontracted_qty: Optional[Decimal] = None





PurchaseOrderItemListResponse = Page[PurchaseOrderItemRead]

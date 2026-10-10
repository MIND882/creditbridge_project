"""Pydantic v2 schemas for QuotationItem."""





from __future__ import annotations

from app.selling.quotation_item_domain.models.quotation_item import (

    QuotationItemMarginType,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "QuotationItemCreate",

    "QuotationItemRead",

    "QuotationItemListResponse",

]





class QuotationItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    is_product_bundle: Optional[bool] = None

    product_bundle_id: Optional[uuid.UUID] = None

    item_name: str

    customer_item_code: Optional[str] = None

    is_free_item: Optional[bool] = None

    is_alternative: Optional[bool] = None

    has_alternative_item: Optional[bool] = None

    description: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Decimal

    stock_uom_id: Optional[uuid.UUID] = None

    uom_id: uuid.UUID

    conversion_factor: Decimal

    stock_qty: Optional[Decimal] = None

    ordered_qty: Decimal

    actual_qty: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    margin_type: Optional[QuotationItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    distributed_discount_amount: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    net_rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    base_rate: Optional[Decimal] = None

    base_net_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    pricing_rules: Optional[str] = None

    stock_uom_rate: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    gross_profit: Optional[Decimal] = None

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    against_blanket_order: Optional[bool] = None

    blanket_order: Optional[str] = None

    blanket_order_rate: Optional[Decimal] = None

    prevdoc_doctype: Optional[str] = None

    prevdoc_docname: Optional[str] = None

    projected_qty: Optional[Decimal] = None

    item_tax_rate: Optional[str] = None

    additional_notes: Optional[str] = None

    page_break: Optional[bool] = None





class QuotationItemCreate(QuotationItemBase):

    pass





class QuotationItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    is_product_bundle: Optional[bool] = None

    product_bundle_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    customer_item_code: Optional[str] = None

    is_free_item: Optional[bool] = None

    is_alternative: Optional[bool] = None

    has_alternative_item: Optional[bool] = None

    description: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    margin_type: Optional[QuotationItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    distributed_discount_amount: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    net_rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    base_rate: Optional[Decimal] = None

    base_net_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    pricing_rules: Optional[str] = None

    stock_uom_rate: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    gross_profit: Optional[Decimal] = None

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    against_blanket_order: Optional[bool] = None

    blanket_order: Optional[str] = None

    blanket_order_rate: Optional[Decimal] = None

    prevdoc_doctype: Optional[str] = None

    prevdoc_docname: Optional[str] = None

    projected_qty: Optional[Decimal] = None

    item_tax_rate: Optional[str] = None

    additional_notes: Optional[str] = None

    page_break: Optional[bool] = None





class QuotationItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    is_product_bundle: Optional[bool] = None

    product_bundle_id: Optional[uuid.UUID] = None

    item_name: str

    customer_item_code: Optional[str] = None

    is_free_item: Optional[bool] = None

    is_alternative: Optional[bool] = None

    has_alternative_item: Optional[bool] = None

    description: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None

    price_list_rate: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    margin_type: Optional[QuotationItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    distributed_discount_amount: Optional[Decimal] = None

    base_rate_with_margin: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    net_rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    base_rate: Optional[Decimal] = None

    base_net_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    pricing_rules: Optional[str] = None

    stock_uom_rate: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    gross_profit: Optional[Decimal] = None

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    against_blanket_order: Optional[bool] = None

    blanket_order: Optional[str] = None

    blanket_order_rate: Optional[Decimal] = None

    prevdoc_doctype: Optional[str] = None

    prevdoc_docname: Optional[str] = None

    projected_qty: Optional[Decimal] = None

    item_tax_rate: Optional[str] = None

    additional_notes: Optional[str] = None

    page_break: Optional[bool] = None





QuotationItemListResponse = Page[QuotationItemRead]

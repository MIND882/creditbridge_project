"""Pydantic v2 schemas for SupplierQuotationItem."""





from __future__ import annotations

from app.buying.supplier_quotation_item_domain.models.supplier_quotation_item import (

    SupplierQuotationItemMarginType,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierQuotationItemCreate",

    "SupplierQuotationItemRead",

    "SupplierQuotationItemListResponse",

]





class SupplierQuotationItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    supplier_part_no: Optional[str] = None

    item_name: Optional[str] = None

    lead_time_days: Optional[int] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Decimal

    stock_uom_id: uuid.UUID

    price_list_rate: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    uom_id: uuid.UUID

    conversion_factor: Decimal

    stock_qty: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    base_rate: Decimal

    base_amount: Decimal

    pricing_rules: Optional[str] = None

    net_rate: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    base_net_rate: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    prevdoc_doctype: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    sales_order: Optional[str] = None

    request_for_quotation_id: Optional[uuid.UUID] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    request_for_quotation_item: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    item_tax_rate: Optional[str] = None

    page_break: Optional[bool] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    is_free_item: Optional[bool] = None

    expected_delivery_date: Optional[dt.date] = None

    cost_center_id: Optional[uuid.UUID] = None

    distributed_discount_amount: Optional[Decimal] = None

    margin_type: Optional[SupplierQuotationItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None





class SupplierQuotationItemCreate(SupplierQuotationItemBase):

    pass





class SupplierQuotationItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    supplier_part_no: Optional[str] = None

    item_name: Optional[str] = None

    lead_time_days: Optional[int] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    price_list_rate: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    base_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    pricing_rules: Optional[str] = None

    net_rate: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    base_net_rate: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    prevdoc_doctype: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    sales_order: Optional[str] = None

    request_for_quotation_id: Optional[uuid.UUID] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    request_for_quotation_item: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    item_tax_rate: Optional[str] = None

    page_break: Optional[bool] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    is_free_item: Optional[bool] = None

    expected_delivery_date: Optional[dt.date] = None

    cost_center_id: Optional[uuid.UUID] = None

    distributed_discount_amount: Optional[Decimal] = None

    margin_type: Optional[SupplierQuotationItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None





class SupplierQuotationItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    supplier_part_no: Optional[str] = None

    item_name: Optional[str] = None

    lead_time_days: Optional[int] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    price_list_rate: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    base_price_list_rate: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    base_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    pricing_rules: Optional[str] = None

    net_rate: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    base_net_rate: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    weight_per_unit: Optional[Decimal] = None

    total_weight: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    prevdoc_doctype: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    sales_order: Optional[str] = None

    request_for_quotation_id: Optional[uuid.UUID] = None

    item_tax_template_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    request_for_quotation_item: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    item_tax_rate: Optional[str] = None

    page_break: Optional[bool] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    is_free_item: Optional[bool] = None

    expected_delivery_date: Optional[dt.date] = None

    cost_center_id: Optional[uuid.UUID] = None

    distributed_discount_amount: Optional[Decimal] = None

    margin_type: Optional[SupplierQuotationItemMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_with_margin: Optional[Decimal] = None





SupplierQuotationItemListResponse = Page[SupplierQuotationItemRead]

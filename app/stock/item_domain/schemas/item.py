"""Pydantic v2 schemas for Item."""





from __future__ import annotations

from app.stock.item_domain.models.item import (

    ItemNamingSeries,

    ItemDefaultMaterialRequestType,

    ItemValuationMethod,

    ItemVariantBasedOn,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.item_barcode_domain.schemas.item_barcode import (

    ItemBarcodeCreate,

    ItemBarcodeRead,

)

from app.stock.item_reorder_domain.schemas.item_reorder import (

    ItemReorderCreate,

    ItemReorderRead,

)

from app.stock.uom_conversion_detail_domain.schemas.uom_conversion_detail import (

    UomConversionDetailCreate,

    UomConversionDetailRead,

)

from app.stock.item_variant_attribute_domain.schemas.item_variant_attribute import (

    ItemVariantAttributeCreate,

    ItemVariantAttributeRead,

)

from app.stock.item_default_domain.schemas.item_default import (

    ItemDefaultCreate,

    ItemDefaultRead,

)

from app.stock.item_supplier_domain.schemas.item_supplier import (

    ItemSupplierCreate,

    ItemSupplierRead,

)

from app.stock.item_customer_detail_domain.schemas.item_customer_detail import (

    ItemCustomerDetailCreate,

    ItemCustomerDetailRead,

)

from app.stock.item_tax_domain.schemas.item_tax import (

    ItemTaxCreate,

    ItemTaxRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemCreate",

    "ItemUpdate",

    "ItemRead",

    "ItemListResponse",

]





class ItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: Optional[ItemNamingSeries] = None

    item_code: str

    variant_of_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    item_group_id: uuid.UUID

    stock_uom_id: uuid.UUID

    disabled: Optional[bool] = None

    allow_alternative_item: Optional[bool] = None

    is_stock_item: Optional[bool] = None

    include_item_in_manufacturing: Optional[bool] = None

    opening_stock: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    standard_rate: Optional[Decimal] = None

    is_fixed_asset: Optional[bool] = None

    asset_category: Optional[str] = None

    asset_naming_series: Optional[str] = None

    image: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    shelf_life_in_days: Optional[int] = None

    end_of_life: Optional[dt.date] = None

    default_material_request_type: Optional[ItemDefaultMaterialRequestType] = None

    valuation_method: Optional[ItemValuationMethod] = None

    warranty_period: Optional[str] = None

    weight_per_unit: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    has_batch_no: Optional[bool] = None

    create_new_batch: Optional[bool] = None

    batch_number_series: Optional[str] = None

    has_expiry_date: Optional[bool] = None

    retain_sample: Optional[bool] = None

    sample_quantity: Optional[int] = None

    has_serial_no: Optional[bool] = None

    serial_no_series: Optional[str] = None

    has_variants: Optional[bool] = None

    variant_based_on: Optional[ItemVariantBasedOn] = None

    is_purchase_item: Optional[bool] = None

    purchase_uom_id: Optional[uuid.UUID] = None

    min_order_qty: Optional[Decimal] = None

    safety_stock: Optional[Decimal] = None

    lead_time_days: Optional[int] = None

    last_purchase_rate: Optional[Decimal] = None

    is_customer_provided_item: Optional[bool] = None

    delivered_by_supplier: Optional[bool] = None

    country_of_origin: Optional[str] = None

    customs_tariff_number_id: Optional[uuid.UUID] = None

    sales_uom_id: Optional[uuid.UUID] = None

    is_sales_item: Optional[bool] = None

    max_discount: Optional[Decimal] = None

    enable_deferred_revenue: Optional[bool] = None

    no_of_months: Optional[int] = None

    enable_deferred_expense: Optional[bool] = None

    no_of_months_exp: Optional[int] = None

    inspection_required_before_purchase: Optional[bool] = None

    inspection_required_before_delivery: Optional[bool] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    default_bom: Optional[str] = None

    is_sub_contracted_item: Optional[bool] = None

    customer_code: Optional[str] = None

    total_projected_qty: Optional[Decimal] = None

    over_delivery_receipt_allowance: Optional[Decimal] = None

    over_billing_allowance: Optional[Decimal] = None

    auto_create_assets: Optional[bool] = None

    default_item_manufacturer_id: Optional[uuid.UUID] = None

    default_manufacturer_part_no: Optional[str] = None

    grant_commission: Optional[bool] = None

    is_grouped_asset: Optional[bool] = None

    allow_negative_stock: Optional[bool] = None

    production_capacity: Optional[int] = None

    purchase_tax_withholding_category_id: Optional[uuid.UUID] = None

    sales_tax_withholding_category_id: Optional[uuid.UUID] = None

    restrict_to_companies: Optional[bool] = None

    barcodes: list[ItemBarcodeCreate] = []

    reorder_levels: list[ItemReorderCreate] = []

    uoms: list[UomConversionDetailCreate] = []

    attributes: list[ItemVariantAttributeCreate] = []

    item_defaults: list[ItemDefaultCreate] = []

    supplier_items: list[ItemSupplierCreate] = []

    customer_items: list[ItemCustomerDetailCreate] = []

    taxes: list[ItemTaxCreate] = []





class ItemCreate(ItemBase):

    pass





class ItemUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[ItemNamingSeries] = None

    item_code: Optional[str] = None

    variant_of_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    disabled: Optional[bool] = None

    allow_alternative_item: Optional[bool] = None

    is_stock_item: Optional[bool] = None

    include_item_in_manufacturing: Optional[bool] = None

    opening_stock: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    standard_rate: Optional[Decimal] = None

    is_fixed_asset: Optional[bool] = None

    asset_category: Optional[str] = None

    asset_naming_series: Optional[str] = None

    image: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    shelf_life_in_days: Optional[int] = None

    end_of_life: Optional[dt.date] = None

    default_material_request_type: Optional[ItemDefaultMaterialRequestType] = None

    valuation_method: Optional[ItemValuationMethod] = None

    warranty_period: Optional[str] = None

    weight_per_unit: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    has_batch_no: Optional[bool] = None

    create_new_batch: Optional[bool] = None

    batch_number_series: Optional[str] = None

    has_expiry_date: Optional[bool] = None

    retain_sample: Optional[bool] = None

    sample_quantity: Optional[int] = None

    has_serial_no: Optional[bool] = None

    serial_no_series: Optional[str] = None

    has_variants: Optional[bool] = None

    variant_based_on: Optional[ItemVariantBasedOn] = None

    is_purchase_item: Optional[bool] = None

    purchase_uom_id: Optional[uuid.UUID] = None

    min_order_qty: Optional[Decimal] = None

    safety_stock: Optional[Decimal] = None

    lead_time_days: Optional[int] = None

    last_purchase_rate: Optional[Decimal] = None

    is_customer_provided_item: Optional[bool] = None

    delivered_by_supplier: Optional[bool] = None

    country_of_origin: Optional[str] = None

    customs_tariff_number_id: Optional[uuid.UUID] = None

    sales_uom_id: Optional[uuid.UUID] = None

    is_sales_item: Optional[bool] = None

    max_discount: Optional[Decimal] = None

    enable_deferred_revenue: Optional[bool] = None

    no_of_months: Optional[int] = None

    enable_deferred_expense: Optional[bool] = None

    no_of_months_exp: Optional[int] = None

    inspection_required_before_purchase: Optional[bool] = None

    inspection_required_before_delivery: Optional[bool] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    default_bom: Optional[str] = None

    is_sub_contracted_item: Optional[bool] = None

    customer_code: Optional[str] = None

    total_projected_qty: Optional[Decimal] = None

    over_delivery_receipt_allowance: Optional[Decimal] = None

    over_billing_allowance: Optional[Decimal] = None

    auto_create_assets: Optional[bool] = None

    default_item_manufacturer_id: Optional[uuid.UUID] = None

    default_manufacturer_part_no: Optional[str] = None

    grant_commission: Optional[bool] = None

    is_grouped_asset: Optional[bool] = None

    allow_negative_stock: Optional[bool] = None

    production_capacity: Optional[int] = None

    purchase_tax_withholding_category_id: Optional[uuid.UUID] = None

    sales_tax_withholding_category_id: Optional[uuid.UUID] = None

    restrict_to_companies: Optional[bool] = None

    barcodes: Optional[list[ItemBarcodeCreate]] = None

    reorder_levels: Optional[list[ItemReorderCreate]] = None

    uoms: Optional[list[UomConversionDetailCreate]] = None

    attributes: Optional[list[ItemVariantAttributeCreate]] = None

    item_defaults: Optional[list[ItemDefaultCreate]] = None

    supplier_items: Optional[list[ItemSupplierCreate]] = None

    customer_items: Optional[list[ItemCustomerDetailCreate]] = None

    taxes: Optional[list[ItemTaxCreate]] = None





class ItemRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[ItemNamingSeries] = None

    item_code: str

    variant_of_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    disabled: Optional[bool] = None

    allow_alternative_item: Optional[bool] = None

    is_stock_item: Optional[bool] = None

    include_item_in_manufacturing: Optional[bool] = None

    opening_stock: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    standard_rate: Optional[Decimal] = None

    is_fixed_asset: Optional[bool] = None

    asset_category: Optional[str] = None

    asset_naming_series: Optional[str] = None

    image: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    shelf_life_in_days: Optional[int] = None

    end_of_life: Optional[dt.date] = None

    default_material_request_type: Optional[ItemDefaultMaterialRequestType] = None

    valuation_method: Optional[ItemValuationMethod] = None

    warranty_period: Optional[str] = None

    weight_per_unit: Optional[Decimal] = None

    weight_uom_id: Optional[uuid.UUID] = None

    has_batch_no: Optional[bool] = None

    create_new_batch: Optional[bool] = None

    batch_number_series: Optional[str] = None

    has_expiry_date: Optional[bool] = None

    retain_sample: Optional[bool] = None

    sample_quantity: Optional[int] = None

    has_serial_no: Optional[bool] = None

    serial_no_series: Optional[str] = None

    has_variants: Optional[bool] = None

    variant_based_on: Optional[ItemVariantBasedOn] = None

    is_purchase_item: Optional[bool] = None

    purchase_uom_id: Optional[uuid.UUID] = None

    min_order_qty: Optional[Decimal] = None

    safety_stock: Optional[Decimal] = None

    lead_time_days: Optional[int] = None

    last_purchase_rate: Optional[Decimal] = None

    is_customer_provided_item: Optional[bool] = None

    delivered_by_supplier: Optional[bool] = None

    country_of_origin: Optional[str] = None

    customs_tariff_number_id: Optional[uuid.UUID] = None

    sales_uom_id: Optional[uuid.UUID] = None

    is_sales_item: Optional[bool] = None

    max_discount: Optional[Decimal] = None

    enable_deferred_revenue: Optional[bool] = None

    no_of_months: Optional[int] = None

    enable_deferred_expense: Optional[bool] = None

    no_of_months_exp: Optional[int] = None

    inspection_required_before_purchase: Optional[bool] = None

    inspection_required_before_delivery: Optional[bool] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    default_bom: Optional[str] = None

    is_sub_contracted_item: Optional[bool] = None

    customer_code: Optional[str] = None

    total_projected_qty: Optional[Decimal] = None

    over_delivery_receipt_allowance: Optional[Decimal] = None

    over_billing_allowance: Optional[Decimal] = None

    auto_create_assets: Optional[bool] = None

    default_item_manufacturer_id: Optional[uuid.UUID] = None

    default_manufacturer_part_no: Optional[str] = None

    grant_commission: Optional[bool] = None

    is_grouped_asset: Optional[bool] = None

    allow_negative_stock: Optional[bool] = None

    production_capacity: Optional[int] = None

    purchase_tax_withholding_category_id: Optional[uuid.UUID] = None

    sales_tax_withholding_category_id: Optional[uuid.UUID] = None

    restrict_to_companies: Optional[bool] = None

    barcodes: list[ItemBarcodeRead] = []

    reorder_levels: list[ItemReorderRead] = []

    uoms: list[UomConversionDetailRead] = []

    attributes: list[ItemVariantAttributeRead] = []

    item_defaults: list[ItemDefaultRead] = []

    supplier_items: list[ItemSupplierRead] = []

    customer_items: list[ItemCustomerDetailRead] = []

    taxes: list[ItemTaxRead] = []





ItemListResponse = Page[ItemRead]

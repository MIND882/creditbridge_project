"""Pydantic v2 schemas for StockSettings."""





from __future__ import annotations

from app.stock.stock_settings_domain.models.stock_settings import (

    StockSettingsItemNamingBy,

    StockSettingsValuationMethod,

    StockSettingsActionIfQualityInspectionIsNotSubmitted,

    StockSettingsActionIfQualityInspectionIsRejected,

    StockSettingsPickSerialAndBatchBasedOn,

    StockSettingsUpdatePriceListBasedOn,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockSettingsUpdate",

    "StockSettingsRead",

]





class StockSettingsUpdate(InputSchema):

    """A partial update of the tenant settings row."""



    item_naming_by: Optional[StockSettingsItemNamingBy] = None

    item_group_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    valuation_method: Optional[StockSettingsValuationMethod] = None

    over_delivery_receipt_allowance: Optional[Decimal] = None

    action_if_quality_inspection_is_not_submitted: Optional[StockSettingsActionIfQualityInspectionIsNotSubmitted] = None

    show_barcode_field: Optional[bool] = None

    clean_description_html: Optional[bool] = None

    auto_insert_price_list_rate_if_missing: Optional[bool] = None

    allow_negative_stock: Optional[bool] = None

    auto_indent: Optional[bool] = None

    reorder_email_notify: Optional[bool] = None

    stock_frozen_upto: Optional[dt.date] = None

    stock_frozen_upto_days: Optional[int] = None

    stock_auth_role: Optional[str] = None

    use_naming_series: Optional[bool] = None

    naming_series_prefix: Optional[str] = None

    role_allowed_to_create_edit_back_dated_transactions: Optional[str] = None

    disable_serial_no_and_batch_selector: Optional[bool] = None

    role_allowed_to_over_deliver_receive: Optional[str] = None

    action_if_quality_inspection_is_rejected: Optional[StockSettingsActionIfQualityInspectionIsRejected] = None

    mr_qty_allowance: Optional[Decimal] = None

    update_existing_price_list_rate: Optional[bool] = None

    enable_stock_reservation: Optional[bool] = None

    allow_partial_reservation: Optional[bool] = None

    pick_serial_and_batch_based_on: Optional[StockSettingsPickSerialAndBatchBasedOn] = None

    auto_create_serial_and_batch_bundle_for_outward: Optional[bool] = None

    auto_reserve_serial_and_batch: Optional[bool] = None

    allow_to_edit_stock_uom_qty_for_sales: Optional[bool] = None

    allow_to_edit_stock_uom_qty_for_purchase: Optional[bool] = None

    allow_to_edit_stock_uom_qty_for_stock_entry: Optional[bool] = None

    auto_reserve_stock_for_sales_order_on_purchase: Optional[bool] = None

    use_serial_batch_fields: Optional[bool] = None

    do_not_update_serial_batch_on_creation_of_auto_bundle: Optional[bool] = None

    allow_internal_transfer_at_arms_length_price: Optional[bool] = None

    do_not_use_batchwise_valuation: Optional[bool] = None

    over_picking_allowance: Optional[Decimal] = None

    allow_existing_serial_no: Optional[bool] = None

    auto_reserve_stock: Optional[bool] = None

    set_serial_and_batch_bundle_naming_based_on_naming_series: Optional[bool] = None

    allow_uom_with_conversion_rate_defined_in_item: Optional[bool] = None

    allow_to_make_quality_inspection_after_purchase_or_delivery: Optional[bool] = None

    update_price_list_based_on: Optional[StockSettingsUpdatePriceListBasedOn] = None

    validate_material_transfer_warehouses: Optional[bool] = None

    allow_negative_stock_for_batch: Optional[bool] = None

    enable_serial_and_batch_no_for_item: Optional[bool] = None

    naming_series_details: Optional[str] = None

    naming_series_preview: Optional[str] = None

    use_inline_serial_batch_editor: Optional[bool] = None





class StockSettingsRead(ReadSchema):

    id: uuid.UUID

    item_naming_by: Optional[StockSettingsItemNamingBy] = None

    item_group_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    valuation_method: Optional[StockSettingsValuationMethod] = None

    over_delivery_receipt_allowance: Optional[Decimal] = None

    action_if_quality_inspection_is_not_submitted: Optional[StockSettingsActionIfQualityInspectionIsNotSubmitted] = None

    show_barcode_field: Optional[bool] = None

    clean_description_html: Optional[bool] = None

    auto_insert_price_list_rate_if_missing: Optional[bool] = None

    allow_negative_stock: Optional[bool] = None

    auto_indent: Optional[bool] = None

    reorder_email_notify: Optional[bool] = None

    stock_frozen_upto: Optional[dt.date] = None

    stock_frozen_upto_days: Optional[int] = None

    stock_auth_role: Optional[str] = None

    use_naming_series: Optional[bool] = None

    naming_series_prefix: Optional[str] = None

    role_allowed_to_create_edit_back_dated_transactions: Optional[str] = None

    disable_serial_no_and_batch_selector: Optional[bool] = None

    role_allowed_to_over_deliver_receive: Optional[str] = None

    action_if_quality_inspection_is_rejected: Optional[StockSettingsActionIfQualityInspectionIsRejected] = None

    mr_qty_allowance: Optional[Decimal] = None

    update_existing_price_list_rate: Optional[bool] = None

    enable_stock_reservation: Optional[bool] = None

    allow_partial_reservation: Optional[bool] = None

    pick_serial_and_batch_based_on: Optional[StockSettingsPickSerialAndBatchBasedOn] = None

    auto_create_serial_and_batch_bundle_for_outward: Optional[bool] = None

    auto_reserve_serial_and_batch: Optional[bool] = None

    allow_to_edit_stock_uom_qty_for_sales: Optional[bool] = None

    allow_to_edit_stock_uom_qty_for_purchase: Optional[bool] = None

    allow_to_edit_stock_uom_qty_for_stock_entry: Optional[bool] = None

    auto_reserve_stock_for_sales_order_on_purchase: Optional[bool] = None

    use_serial_batch_fields: Optional[bool] = None

    do_not_update_serial_batch_on_creation_of_auto_bundle: Optional[bool] = None

    allow_internal_transfer_at_arms_length_price: Optional[bool] = None

    do_not_use_batchwise_valuation: Optional[bool] = None

    over_picking_allowance: Optional[Decimal] = None

    allow_existing_serial_no: Optional[bool] = None

    auto_reserve_stock: Optional[bool] = None

    set_serial_and_batch_bundle_naming_based_on_naming_series: Optional[bool] = None

    allow_uom_with_conversion_rate_defined_in_item: Optional[bool] = None

    allow_to_make_quality_inspection_after_purchase_or_delivery: Optional[bool] = None

    update_price_list_based_on: Optional[StockSettingsUpdatePriceListBasedOn] = None

    validate_material_transfer_warehouses: Optional[bool] = None

    allow_negative_stock_for_batch: Optional[bool] = None

    enable_serial_and_batch_no_for_item: Optional[bool] = None

    naming_series_details: Optional[str] = None

    naming_series_preview: Optional[str] = None

    use_inline_serial_batch_editor: Optional[bool] = None



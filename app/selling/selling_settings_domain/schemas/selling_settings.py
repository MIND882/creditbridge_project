"""Pydantic v2 schemas for SellingSettings."""





from __future__ import annotations

from app.selling.selling_settings_domain.models.selling_settings import (

    SellingSettingsCustMasterName,

    SellingSettingsMaintainSameRateAction,

    SellingSettingsSoRequired,

    SellingSettingsDnRequired,

    SellingSettingsSalesUpdateFrequency,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SellingSettingsUpdate",

    "SellingSettingsRead",

]





class SellingSettingsUpdate(InputSchema):

    """A partial update of the tenant settings row."""



    cust_master_name: Optional[SellingSettingsCustMasterName] = None

    naming_series_details: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    selling_price_list_id: Optional[uuid.UUID] = None

    fallback_to_default_price_list: Optional[bool] = None

    editable_price_list_rate: Optional[bool] = None

    maintain_same_sales_rate: Optional[bool] = None

    maintain_same_rate_action: Optional[SellingSettingsMaintainSameRateAction] = None

    role_to_override_stop_action: Optional[str] = None

    validate_selling_price: Optional[bool] = None

    editable_bundle_item_rates: Optional[bool] = None

    allow_negative_rates_for_items: Optional[bool] = None

    so_required: Optional[SellingSettingsSoRequired] = None

    dn_required: Optional[SellingSettingsDnRequired] = None

    sales_update_frequency: Optional[SellingSettingsSalesUpdateFrequency] = None

    allow_multiple_items: Optional[bool] = None

    allow_against_multiple_purchase_orders: Optional[bool] = None

    hide_tax_id: Optional[bool] = None

    allow_sales_order_creation_for_expired_quotation: Optional[bool] = None

    dont_reserve_sales_order_qty_on_sales_return: Optional[bool] = None

    enable_cutoff_date_on_bulk_delivery_note_creation: Optional[bool] = None

    set_zero_rate_for_expired_batch: Optional[bool] = None

    allow_zero_qty_in_quotation: Optional[bool] = None

    allow_zero_qty_in_sales_order: Optional[bool] = None

    blanket_order_allowance: Optional[Decimal] = None

    enable_proforma_invoice: Optional[bool] = None

    default_proforma_print_format: Optional[str] = None

    enable_tracking_sales_commissions: Optional[bool] = None

    enable_discount_accounting: Optional[bool] = None

    enable_utm: Optional[bool] = None

    use_legacy_js_reactivity: Optional[bool] = None

    allow_delivery_of_overproduced_qty: Optional[bool] = None

    deliver_secondary_items: Optional[bool] = None





class SellingSettingsRead(ReadSchema):

    id: uuid.UUID

    cust_master_name: Optional[SellingSettingsCustMasterName] = None

    naming_series_details: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    selling_price_list_id: Optional[uuid.UUID] = None

    fallback_to_default_price_list: Optional[bool] = None

    editable_price_list_rate: Optional[bool] = None

    maintain_same_sales_rate: Optional[bool] = None

    maintain_same_rate_action: Optional[SellingSettingsMaintainSameRateAction] = None

    role_to_override_stop_action: Optional[str] = None

    validate_selling_price: Optional[bool] = None

    editable_bundle_item_rates: Optional[bool] = None

    allow_negative_rates_for_items: Optional[bool] = None

    so_required: Optional[SellingSettingsSoRequired] = None

    dn_required: Optional[SellingSettingsDnRequired] = None

    sales_update_frequency: Optional[SellingSettingsSalesUpdateFrequency] = None

    allow_multiple_items: Optional[bool] = None

    allow_against_multiple_purchase_orders: Optional[bool] = None

    hide_tax_id: Optional[bool] = None

    allow_sales_order_creation_for_expired_quotation: Optional[bool] = None

    dont_reserve_sales_order_qty_on_sales_return: Optional[bool] = None

    enable_cutoff_date_on_bulk_delivery_note_creation: Optional[bool] = None

    set_zero_rate_for_expired_batch: Optional[bool] = None

    allow_zero_qty_in_quotation: Optional[bool] = None

    allow_zero_qty_in_sales_order: Optional[bool] = None

    blanket_order_allowance: Optional[Decimal] = None

    enable_proforma_invoice: Optional[bool] = None

    default_proforma_print_format: Optional[str] = None

    enable_tracking_sales_commissions: Optional[bool] = None

    enable_discount_accounting: Optional[bool] = None

    enable_utm: Optional[bool] = None

    use_legacy_js_reactivity: Optional[bool] = None

    allow_delivery_of_overproduced_qty: Optional[bool] = None

    deliver_secondary_items: Optional[bool] = None



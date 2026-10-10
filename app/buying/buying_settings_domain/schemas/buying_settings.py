"""Pydantic v2 schemas for BuyingSettings."""





from __future__ import annotations

from app.buying.buying_settings_domain.models.buying_settings import (

    BuyingSettingsSuppMasterName,

    BuyingSettingsPoRequired,

    BuyingSettingsPrRequired,

    BuyingSettingsBackflushRawMaterialsOfSubcontractBasedOn,

    BuyingSettingsMaintainSameRateAction,

    BuyingSettingsProjectUpdateFrequency,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BuyingSettingsUpdate",

    "BuyingSettingsRead",

]





class BuyingSettingsUpdate(InputSchema):

    """A partial update of the tenant settings row."""



    supp_master_name: Optional[BuyingSettingsSuppMasterName] = None

    supplier_group: Optional[str] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    po_required: Optional[BuyingSettingsPoRequired] = None

    pr_required: Optional[BuyingSettingsPrRequired] = None

    maintain_same_rate: Optional[bool] = None

    allow_multiple_items: Optional[bool] = None

    backflush_raw_materials_of_subcontract_based_on: Optional[BuyingSettingsBackflushRawMaterialsOfSubcontractBasedOn] = None

    over_transfer_allowance: Optional[Decimal] = None

    maintain_same_rate_action: Optional[BuyingSettingsMaintainSameRateAction] = None

    role_to_override_stop_action: Optional[str] = None

    bill_for_rejected_quantity_in_purchase_invoice: Optional[bool] = None

    disable_last_purchase_rate: Optional[bool] = None

    show_pay_button: Optional[bool] = None

    set_landed_cost_based_on_purchase_invoice_rate: Optional[bool] = None

    use_transaction_date_exchange_rate: Optional[bool] = None

    blanket_order_allowance: Optional[Decimal] = None

    auto_create_subcontracting_order: Optional[bool] = None

    auto_create_purchase_receipt: Optional[bool] = None

    project_update_frequency: Optional[BuyingSettingsProjectUpdateFrequency] = None

    allow_zero_qty_in_purchase_order: Optional[bool] = None

    allow_zero_qty_in_request_for_quotation: Optional[bool] = None

    allow_zero_qty_in_supplier_quotation: Optional[bool] = None

    set_valuation_rate_for_rejected_materials: Optional[bool] = None

    fixed_email: Optional[str] = None

    validate_consumed_qty: Optional[bool] = None

    allow_negative_rates_for_items: Optional[bool] = None

    naming_series_details: Optional[str] = None

    over_order_allowance: Optional[Decimal] = None





class BuyingSettingsRead(ReadSchema):

    id: uuid.UUID

    supp_master_name: Optional[BuyingSettingsSuppMasterName] = None

    supplier_group: Optional[str] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    po_required: Optional[BuyingSettingsPoRequired] = None

    pr_required: Optional[BuyingSettingsPrRequired] = None

    maintain_same_rate: Optional[bool] = None

    allow_multiple_items: Optional[bool] = None

    backflush_raw_materials_of_subcontract_based_on: Optional[BuyingSettingsBackflushRawMaterialsOfSubcontractBasedOn] = None

    over_transfer_allowance: Optional[Decimal] = None

    maintain_same_rate_action: Optional[BuyingSettingsMaintainSameRateAction] = None

    role_to_override_stop_action: Optional[str] = None

    bill_for_rejected_quantity_in_purchase_invoice: Optional[bool] = None

    disable_last_purchase_rate: Optional[bool] = None

    show_pay_button: Optional[bool] = None

    set_landed_cost_based_on_purchase_invoice_rate: Optional[bool] = None

    use_transaction_date_exchange_rate: Optional[bool] = None

    blanket_order_allowance: Optional[Decimal] = None

    auto_create_subcontracting_order: Optional[bool] = None

    auto_create_purchase_receipt: Optional[bool] = None

    project_update_frequency: Optional[BuyingSettingsProjectUpdateFrequency] = None

    allow_zero_qty_in_purchase_order: Optional[bool] = None

    allow_zero_qty_in_request_for_quotation: Optional[bool] = None

    allow_zero_qty_in_supplier_quotation: Optional[bool] = None

    set_valuation_rate_for_rejected_materials: Optional[bool] = None

    fixed_email: Optional[str] = None

    validate_consumed_qty: Optional[bool] = None

    allow_negative_rates_for_items: Optional[bool] = None

    naming_series_details: Optional[str] = None

    over_order_allowance: Optional[Decimal] = None



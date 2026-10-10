"""Pydantic v2 schemas for StockEntryDetail."""





from __future__ import annotations

from app.stock.stock_entry_detail_domain.models.stock_entry_detail import (

    StockEntryDetailSecondaryItemType,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockEntryDetailCreate",

    "StockEntryDetailRead",

    "StockEntryDetailListResponse",

]





class StockEntryDetailBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    barcode: Optional[str] = None

    s_warehouse_id: Optional[uuid.UUID] = None

    t_warehouse_id: Optional[uuid.UUID] = None

    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Decimal

    basic_rate: Optional[Decimal] = None

    basic_amount: Optional[Decimal] = None

    additional_cost: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    uom_id: uuid.UUID

    conversion_factor: Decimal

    stock_uom_id: uuid.UUID

    transfer_qty: Optional[Decimal] = None

    retain_sample: Optional[bool] = None

    sample_quantity: Optional[int] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    allow_zero_valuation_rate: Optional[bool] = None

    actual_qty: Optional[Decimal] = None

    bom_no: Optional[str] = None

    allow_alternative_item: Optional[bool] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item_id: Optional[uuid.UUID] = None

    pick_list_item_id: Optional[uuid.UUID] = None

    original_item_id: Optional[uuid.UUID] = None

    subcontracted_item_id: Optional[uuid.UUID] = None

    against_stock_entry_id: Optional[uuid.UUID] = None

    ste_detail: Optional[str] = None

    transferred_qty: Optional[Decimal] = None

    item_group: Optional[str] = None

    reference_purchase_receipt_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    po_detail: Optional[str] = None

    sco_rm_detail: Optional[str] = None

    set_basic_rate_manually: Optional[bool] = None

    putaway_rule_id: Optional[uuid.UUID] = None

    is_finished_item: Optional[bool] = None

    job_card_item: Optional[str] = None

    has_item_scanned: Optional[bool] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    landed_cost_voucher_amount: Optional[Decimal] = None

    customer_provided_item_cost: Optional[Decimal] = None

    scio_detail: Optional[str] = None

    against_fg: Optional[str] = None

    secondary_item_type: Optional[StockEntryDetailSecondaryItemType] = None

    bom_secondary_item: Optional[str] = None

    is_legacy_scrap_item: Optional[bool] = None





class StockEntryDetailCreate(StockEntryDetailBase):

    pass





class StockEntryDetailUpdate(InputSchema):

    """A partial update."""



    barcode: Optional[str] = None

    s_warehouse_id: Optional[uuid.UUID] = None

    t_warehouse_id: Optional[uuid.UUID] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    basic_rate: Optional[Decimal] = None

    basic_amount: Optional[Decimal] = None

    additional_cost: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    transfer_qty: Optional[Decimal] = None

    retain_sample: Optional[bool] = None

    sample_quantity: Optional[int] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    allow_zero_valuation_rate: Optional[bool] = None

    actual_qty: Optional[Decimal] = None

    bom_no: Optional[str] = None

    allow_alternative_item: Optional[bool] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item_id: Optional[uuid.UUID] = None

    pick_list_item_id: Optional[uuid.UUID] = None

    original_item_id: Optional[uuid.UUID] = None

    subcontracted_item_id: Optional[uuid.UUID] = None

    against_stock_entry_id: Optional[uuid.UUID] = None

    ste_detail: Optional[str] = None

    transferred_qty: Optional[Decimal] = None

    item_group: Optional[str] = None

    reference_purchase_receipt_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    po_detail: Optional[str] = None

    sco_rm_detail: Optional[str] = None

    set_basic_rate_manually: Optional[bool] = None

    putaway_rule_id: Optional[uuid.UUID] = None

    is_finished_item: Optional[bool] = None

    job_card_item: Optional[str] = None

    has_item_scanned: Optional[bool] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    landed_cost_voucher_amount: Optional[Decimal] = None

    customer_provided_item_cost: Optional[Decimal] = None

    scio_detail: Optional[str] = None

    against_fg: Optional[str] = None

    secondary_item_type: Optional[StockEntryDetailSecondaryItemType] = None

    bom_secondary_item: Optional[str] = None

    is_legacy_scrap_item: Optional[bool] = None





class StockEntryDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    barcode: Optional[str] = None

    s_warehouse_id: Optional[uuid.UUID] = None

    t_warehouse_id: Optional[uuid.UUID] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    basic_rate: Optional[Decimal] = None

    basic_amount: Optional[Decimal] = None

    additional_cost: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    valuation_rate: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    transfer_qty: Optional[Decimal] = None

    retain_sample: Optional[bool] = None

    sample_quantity: Optional[int] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    quality_inspection_id: Optional[uuid.UUID] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    allow_zero_valuation_rate: Optional[bool] = None

    actual_qty: Optional[Decimal] = None

    bom_no: Optional[str] = None

    allow_alternative_item: Optional[bool] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item_id: Optional[uuid.UUID] = None

    pick_list_item_id: Optional[uuid.UUID] = None

    original_item_id: Optional[uuid.UUID] = None

    subcontracted_item_id: Optional[uuid.UUID] = None

    against_stock_entry_id: Optional[uuid.UUID] = None

    ste_detail: Optional[str] = None

    transferred_qty: Optional[Decimal] = None

    item_group: Optional[str] = None

    reference_purchase_receipt_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    po_detail: Optional[str] = None

    sco_rm_detail: Optional[str] = None

    set_basic_rate_manually: Optional[bool] = None

    putaway_rule_id: Optional[uuid.UUID] = None

    is_finished_item: Optional[bool] = None

    job_card_item: Optional[str] = None

    has_item_scanned: Optional[bool] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    landed_cost_voucher_amount: Optional[Decimal] = None

    customer_provided_item_cost: Optional[Decimal] = None

    scio_detail: Optional[str] = None

    against_fg: Optional[str] = None

    secondary_item_type: Optional[StockEntryDetailSecondaryItemType] = None

    bom_secondary_item: Optional[str] = None

    is_legacy_scrap_item: Optional[bool] = None





StockEntryDetailListResponse = Page[StockEntryDetailRead]

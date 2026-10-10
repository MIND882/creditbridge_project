"""Pydantic v2 schemas for StockEntry."""





from __future__ import annotations

from app.stock.stock_entry_domain.models.stock_entry import (

    StockEntryNamingSeries,

    StockEntryPurpose,

    StockEntryIsOpening,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.stock_entry_detail_domain.schemas.stock_entry_detail import (

    StockEntryDetailCreate,

    StockEntryDetailRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockEntryCreate",

    "StockEntryUpdate",

    "StockEntryRead",

    "StockEntryListResponse",

]





class StockEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: StockEntryNamingSeries

    stock_entry_type_id: uuid.UUID

    outgoing_stock_entry_id: Optional[uuid.UUID] = None

    source_stock_entry_id: Optional[uuid.UUID] = None

    purpose: Optional[StockEntryPurpose] = None

    company: str

    work_order: Optional[str] = None

    purchase_order: Optional[str] = None

    subcontracting_order: Optional[str] = None

    delivery_note_no_id: Optional[uuid.UUID] = None

    sales_invoice_no_id: Optional[uuid.UUID] = None

    purchase_receipt_no_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    inspection_required: Optional[bool] = None

    from_bom: Optional[bool] = None

    bom_no: Optional[str] = None

    fg_completed_qty: Optional[Decimal] = None

    use_multi_level_bom: Optional[bool] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    source_warehouse_address: Optional[str] = None

    source_address_display: Optional[str] = None

    to_warehouse_id: Optional[uuid.UUID] = None

    target_warehouse_address: Optional[str] = None

    target_address_display: Optional[str] = None

    scan_barcode: Optional[str] = None

    total_incoming_value: Optional[Decimal] = None

    total_outgoing_value: Optional[Decimal] = None

    value_difference: Optional[Decimal] = None

    total_additional_costs: Optional[Decimal] = None

    supplier: Optional[str] = None

    supplier_name: Optional[str] = None

    supplier_address: Optional[str] = None

    address_display: Optional[str] = None

    select_print_heading: Optional[str] = None

    letter_head: Optional[str] = None

    is_opening: Optional[StockEntryIsOpening] = None

    project: Optional[str] = None

    remarks: Optional[str] = None

    per_transferred: Optional[Decimal] = None

    total_amount: Optional[Decimal] = None

    job_card: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    credit_note_id: Optional[uuid.UUID] = None

    pick_list_id: Optional[uuid.UUID] = None

    add_to_transit: Optional[bool] = None

    apply_putaway_rule: Optional[bool] = None

    is_return: Optional[bool] = None

    process_loss_qty: Optional[Decimal] = None

    process_loss_percentage: Optional[Decimal] = None

    asset_repair: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    is_additional_transfer_entry: Optional[bool] = None

    subcontracting_inward_order: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    items: list[StockEntryDetailCreate] = []





class StockEntryCreate(StockEntryBase):

    pass





class StockEntryUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[StockEntryNamingSeries] = None

    stock_entry_type_id: Optional[uuid.UUID] = None

    outgoing_stock_entry_id: Optional[uuid.UUID] = None

    source_stock_entry_id: Optional[uuid.UUID] = None

    purpose: Optional[StockEntryPurpose] = None

    company: Optional[str] = None

    work_order: Optional[str] = None

    purchase_order: Optional[str] = None

    subcontracting_order: Optional[str] = None

    delivery_note_no_id: Optional[uuid.UUID] = None

    sales_invoice_no_id: Optional[uuid.UUID] = None

    purchase_receipt_no_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    inspection_required: Optional[bool] = None

    from_bom: Optional[bool] = None

    bom_no: Optional[str] = None

    fg_completed_qty: Optional[Decimal] = None

    use_multi_level_bom: Optional[bool] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    source_warehouse_address: Optional[str] = None

    source_address_display: Optional[str] = None

    to_warehouse_id: Optional[uuid.UUID] = None

    target_warehouse_address: Optional[str] = None

    target_address_display: Optional[str] = None

    scan_barcode: Optional[str] = None

    total_incoming_value: Optional[Decimal] = None

    total_outgoing_value: Optional[Decimal] = None

    value_difference: Optional[Decimal] = None

    total_additional_costs: Optional[Decimal] = None

    supplier: Optional[str] = None

    supplier_name: Optional[str] = None

    supplier_address: Optional[str] = None

    address_display: Optional[str] = None

    select_print_heading: Optional[str] = None

    letter_head: Optional[str] = None

    is_opening: Optional[StockEntryIsOpening] = None

    project: Optional[str] = None

    remarks: Optional[str] = None

    per_transferred: Optional[Decimal] = None

    total_amount: Optional[Decimal] = None

    job_card: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    credit_note_id: Optional[uuid.UUID] = None

    pick_list_id: Optional[uuid.UUID] = None

    add_to_transit: Optional[bool] = None

    apply_putaway_rule: Optional[bool] = None

    is_return: Optional[bool] = None

    process_loss_qty: Optional[Decimal] = None

    process_loss_percentage: Optional[Decimal] = None

    asset_repair: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    is_additional_transfer_entry: Optional[bool] = None

    subcontracting_inward_order: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    items: Optional[list[StockEntryDetailCreate]] = None





class StockEntryRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[StockEntryNamingSeries] = None

    stock_entry_type_id: Optional[uuid.UUID] = None

    outgoing_stock_entry_id: Optional[uuid.UUID] = None

    source_stock_entry_id: Optional[uuid.UUID] = None

    purpose: Optional[StockEntryPurpose] = None

    company: str

    work_order: Optional[str] = None

    purchase_order: Optional[str] = None

    subcontracting_order: Optional[str] = None

    delivery_note_no_id: Optional[uuid.UUID] = None

    sales_invoice_no_id: Optional[uuid.UUID] = None

    purchase_receipt_no_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    inspection_required: Optional[bool] = None

    from_bom: Optional[bool] = None

    bom_no: Optional[str] = None

    fg_completed_qty: Optional[Decimal] = None

    use_multi_level_bom: Optional[bool] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    source_warehouse_address: Optional[str] = None

    source_address_display: Optional[str] = None

    to_warehouse_id: Optional[uuid.UUID] = None

    target_warehouse_address: Optional[str] = None

    target_address_display: Optional[str] = None

    scan_barcode: Optional[str] = None

    total_incoming_value: Optional[Decimal] = None

    total_outgoing_value: Optional[Decimal] = None

    value_difference: Optional[Decimal] = None

    total_additional_costs: Optional[Decimal] = None

    supplier: Optional[str] = None

    supplier_name: Optional[str] = None

    supplier_address: Optional[str] = None

    address_display: Optional[str] = None

    select_print_heading: Optional[str] = None

    letter_head: Optional[str] = None

    is_opening: Optional[StockEntryIsOpening] = None

    project: Optional[str] = None

    remarks: Optional[str] = None

    per_transferred: Optional[Decimal] = None

    total_amount: Optional[Decimal] = None

    job_card: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    credit_note_id: Optional[uuid.UUID] = None

    pick_list_id: Optional[uuid.UUID] = None

    add_to_transit: Optional[bool] = None

    apply_putaway_rule: Optional[bool] = None

    is_return: Optional[bool] = None

    process_loss_qty: Optional[Decimal] = None

    process_loss_percentage: Optional[Decimal] = None

    asset_repair: Optional[str] = None

    last_scanned_warehouse: Optional[str] = None

    is_additional_transfer_entry: Optional[bool] = None

    subcontracting_inward_order: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[StockEntryDetailRead] = []





StockEntryListResponse = Page[StockEntryRead]

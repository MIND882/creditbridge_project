"""Pydantic v2 schemas for StockReconciliationItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockReconciliationItemCreate",

    "StockReconciliationItemRead",

    "StockReconciliationItemListResponse",

]





class StockReconciliationItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    barcode: Optional[str] = None

    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    warehouse_id: uuid.UUID

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    valuation_rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    serial_no: Optional[str] = None

    current_qty: Optional[Decimal] = None

    current_serial_no: Optional[str] = None

    current_valuation_rate: Optional[Decimal] = None

    current_amount: Optional[Decimal] = None

    quantity_difference: Optional[str] = None

    amount_difference: Optional[Decimal] = None

    batch_no_id: Optional[uuid.UUID] = None

    allow_zero_valuation_rate: Optional[bool] = None

    has_item_scanned: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    current_serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    reconcile_all_serial_batch: Optional[bool] = None





class StockReconciliationItemCreate(StockReconciliationItemBase):

    pass





class StockReconciliationItemUpdate(InputSchema):

    """A partial update."""



    barcode: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    valuation_rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    serial_no: Optional[str] = None

    current_qty: Optional[Decimal] = None

    current_serial_no: Optional[str] = None

    current_valuation_rate: Optional[Decimal] = None

    current_amount: Optional[Decimal] = None

    quantity_difference: Optional[str] = None

    amount_difference: Optional[Decimal] = None

    batch_no_id: Optional[uuid.UUID] = None

    allow_zero_valuation_rate: Optional[bool] = None

    has_item_scanned: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    current_serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    reconcile_all_serial_batch: Optional[bool] = None





class StockReconciliationItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    barcode: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    valuation_rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    serial_no: Optional[str] = None

    current_qty: Optional[Decimal] = None

    current_serial_no: Optional[str] = None

    current_valuation_rate: Optional[Decimal] = None

    current_amount: Optional[Decimal] = None

    quantity_difference: Optional[str] = None

    amount_difference: Optional[Decimal] = None

    batch_no_id: Optional[uuid.UUID] = None

    allow_zero_valuation_rate: Optional[bool] = None

    has_item_scanned: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    current_serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    reconcile_all_serial_batch: Optional[bool] = None





StockReconciliationItemListResponse = Page[StockReconciliationItemRead]

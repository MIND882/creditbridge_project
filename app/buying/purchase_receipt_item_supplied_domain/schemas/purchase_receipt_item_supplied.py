"""Pydantic v2 schemas for PurchaseReceiptItemSupplied."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PurchaseReceiptItemSuppliedCreate",

    "PurchaseReceiptItemSuppliedRead",

    "PurchaseReceiptItemSuppliedListResponse",

]





class PurchaseReceiptItemSuppliedBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    main_item_code_id: Optional[uuid.UUID] = None

    rm_item_code_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    required_qty: Optional[Decimal] = None

    consumed_qty: Decimal

    stock_uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    current_stock: Optional[Decimal] = None

    reference_name: Optional[str] = None

    bom_detail_no: Optional[str] = None

    item_name: Optional[str] = None

    purchase_order_id: Optional[uuid.UUID] = None





class PurchaseReceiptItemSuppliedCreate(PurchaseReceiptItemSuppliedBase):

    pass





class PurchaseReceiptItemSuppliedUpdate(InputSchema):

    """A partial update."""



    main_item_code_id: Optional[uuid.UUID] = None

    rm_item_code_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    required_qty: Optional[Decimal] = None

    consumed_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    current_stock: Optional[Decimal] = None

    reference_name: Optional[str] = None

    bom_detail_no: Optional[str] = None

    item_name: Optional[str] = None

    purchase_order_id: Optional[uuid.UUID] = None





class PurchaseReceiptItemSuppliedRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    main_item_code_id: Optional[uuid.UUID] = None

    rm_item_code_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    required_qty: Optional[Decimal] = None

    consumed_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    current_stock: Optional[Decimal] = None

    reference_name: Optional[str] = None

    bom_detail_no: Optional[str] = None

    item_name: Optional[str] = None

    purchase_order_id: Optional[uuid.UUID] = None





PurchaseReceiptItemSuppliedListResponse = Page[PurchaseReceiptItemSuppliedRead]

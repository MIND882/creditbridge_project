"""Pydantic v2 schemas for LandedCostItem."""





from __future__ import annotations

from app.stock.landed_cost_item_domain.models.landed_cost_item import (

    LandedCostItemReceiptDocumentType,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LandedCostItemCreate",

    "LandedCostItemRead",

    "LandedCostItemListResponse",

]





class LandedCostItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    description: Optional[str] = None

    receipt_document_type: Optional[LandedCostItemReceiptDocumentType] = None

    receipt_document: Optional[str] = None

    qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    amount: Decimal

    applicable_charges: Optional[Decimal] = None

    purchase_receipt_item: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    is_fixed_asset: Optional[bool] = None

    stock_entry_item: Optional[str] = None





class LandedCostItemCreate(LandedCostItemBase):

    pass





class LandedCostItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    receipt_document_type: Optional[LandedCostItemReceiptDocumentType] = None

    receipt_document: Optional[str] = None

    qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    applicable_charges: Optional[Decimal] = None

    purchase_receipt_item: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    is_fixed_asset: Optional[bool] = None

    stock_entry_item: Optional[str] = None





class LandedCostItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    receipt_document_type: Optional[LandedCostItemReceiptDocumentType] = None

    receipt_document: Optional[str] = None

    qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    applicable_charges: Optional[Decimal] = None

    purchase_receipt_item: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    is_fixed_asset: Optional[bool] = None

    stock_entry_item: Optional[str] = None





LandedCostItemListResponse = Page[LandedCostItemRead]

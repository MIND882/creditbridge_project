"""Pydantic v2 schemas for BomExplosionItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomExplosionItemCreate",

    "BomExplosionItemRead",

    "BomExplosionItemListResponse",

]





class BomExplosionItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    operation_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    stock_qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    qty_consumed_per_unit: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    amount: Optional[Decimal] = None

    include_item_in_manufacturing: Optional[bool] = None

    sourced_by_supplier: Optional[bool] = None

    is_sub_assembly_item: Optional[bool] = None





class BomExplosionItemCreate(BomExplosionItemBase):

    pass





class BomExplosionItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    operation_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    stock_qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    qty_consumed_per_unit: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    amount: Optional[Decimal] = None

    include_item_in_manufacturing: Optional[bool] = None

    sourced_by_supplier: Optional[bool] = None

    is_sub_assembly_item: Optional[bool] = None





class BomExplosionItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    operation_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    stock_qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    qty_consumed_per_unit: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    amount: Optional[Decimal] = None

    include_item_in_manufacturing: Optional[bool] = None

    sourced_by_supplier: Optional[bool] = None

    is_sub_assembly_item: Optional[bool] = None





BomExplosionItemListResponse = Page[BomExplosionItemRead]

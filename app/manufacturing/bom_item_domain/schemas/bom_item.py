"""Pydantic v2 schemas for BomItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomItemCreate",

    "BomItemRead",

    "BomItemListResponse",

]





class BomItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    operation_id: Optional[uuid.UUID] = None

    operation_row_id: Optional[int] = None

    do_not_explode: Optional[bool] = None

    bom_no_id: Optional[uuid.UUID] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    allow_alternative_item: Optional[bool] = None

    is_stock_item: Optional[bool] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Decimal

    uom_id: uuid.UUID

    stock_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    rate: Decimal

    base_rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    qty_consumed_per_unit: Optional[Decimal] = None

    has_variants: Optional[bool] = None

    include_item_in_manufacturing: Optional[bool] = None

    original_item_id: Optional[uuid.UUID] = None

    sourced_by_supplier: Optional[bool] = None

    is_sub_assembly_item: Optional[bool] = None

    is_phantom_item: Optional[bool] = None





class BomItemCreate(BomItemBase):

    pass





class BomItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    operation_id: Optional[uuid.UUID] = None

    operation_row_id: Optional[int] = None

    do_not_explode: Optional[bool] = None

    bom_no_id: Optional[uuid.UUID] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    allow_alternative_item: Optional[bool] = None

    is_stock_item: Optional[bool] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    stock_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    base_rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    qty_consumed_per_unit: Optional[Decimal] = None

    has_variants: Optional[bool] = None

    include_item_in_manufacturing: Optional[bool] = None

    original_item_id: Optional[uuid.UUID] = None

    sourced_by_supplier: Optional[bool] = None

    is_sub_assembly_item: Optional[bool] = None

    is_phantom_item: Optional[bool] = None





class BomItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    operation_id: Optional[uuid.UUID] = None

    operation_row_id: Optional[int] = None

    do_not_explode: Optional[bool] = None

    bom_no_id: Optional[uuid.UUID] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    allow_alternative_item: Optional[bool] = None

    is_stock_item: Optional[bool] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    stock_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    base_rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    qty_consumed_per_unit: Optional[Decimal] = None

    has_variants: Optional[bool] = None

    include_item_in_manufacturing: Optional[bool] = None

    original_item_id: Optional[uuid.UUID] = None

    sourced_by_supplier: Optional[bool] = None

    is_sub_assembly_item: Optional[bool] = None

    is_phantom_item: Optional[bool] = None





BomItemListResponse = Page[BomItemRead]

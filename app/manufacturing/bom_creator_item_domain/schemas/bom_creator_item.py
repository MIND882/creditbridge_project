"""Pydantic v2 schemas for BomCreatorItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomCreatorItemCreate",

    "BomCreatorItemRead",

    "BomCreatorItemListResponse",

]





class BomCreatorItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    fg_item_id: uuid.UUID

    is_expandable: Optional[bool] = None

    sourced_by_supplier: Optional[bool] = None

    bom_created: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    is_phantom_item: Optional[bool] = None

    operation_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    stock_qty: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    amount: Optional[Decimal] = None

    base_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    do_not_explode: Optional[bool] = None

    parent_row_no: Optional[str] = None

    fg_reference_id: Optional[str] = None

    instruction: Optional[str] = None





class BomCreatorItemCreate(BomCreatorItemBase):

    pass





class BomCreatorItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    fg_item_id: Optional[uuid.UUID] = None

    is_expandable: Optional[bool] = None

    sourced_by_supplier: Optional[bool] = None

    bom_created: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    is_phantom_item: Optional[bool] = None

    operation_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    stock_qty: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    amount: Optional[Decimal] = None

    base_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    do_not_explode: Optional[bool] = None

    parent_row_no: Optional[str] = None

    fg_reference_id: Optional[str] = None

    instruction: Optional[str] = None





class BomCreatorItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    fg_item_id: Optional[uuid.UUID] = None

    is_expandable: Optional[bool] = None

    sourced_by_supplier: Optional[bool] = None

    bom_created: Optional[bool] = None

    is_subcontracted: Optional[bool] = None

    is_phantom_item: Optional[bool] = None

    operation_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    qty: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    stock_qty: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    amount: Optional[Decimal] = None

    base_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    do_not_explode: Optional[bool] = None

    parent_row_no: Optional[str] = None

    fg_reference_id: Optional[str] = None

    instruction: Optional[str] = None





BomCreatorItemListResponse = Page[BomCreatorItemRead]

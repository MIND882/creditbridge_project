"""Pydantic v2 schemas for BomSecondaryItem."""





from __future__ import annotations

from app.manufacturing.bom_secondary_item_domain.models.bom_secondary_item import (

    BomSecondaryItemSecondaryItemType,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomSecondaryItemCreate",

    "BomSecondaryItemRead",

    "BomSecondaryItemListResponse",

]





class BomSecondaryItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    rate: Optional[Decimal] = None

    is_legacy: Optional[bool] = None

    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    secondary_item_type: Optional[BomSecondaryItemSecondaryItemType] = None

    uom_id: uuid.UUID

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    conversion_factor: Decimal

    stock_qty: Optional[Decimal] = None

    image: Optional[str] = None

    description: Optional[str] = None

    image_nygv: Optional[str] = None

    cost_allocation_per: Decimal

    process_loss_per: Decimal

    cost: Decimal

    base_cost: Decimal

    process_loss_qty: Decimal





class BomSecondaryItemCreate(BomSecondaryItemBase):

    pass





class BomSecondaryItemUpdate(InputSchema):

    """A partial update."""



    rate: Optional[Decimal] = None

    is_legacy: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    secondary_item_type: Optional[BomSecondaryItemSecondaryItemType] = None

    uom_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    image: Optional[str] = None

    description: Optional[str] = None

    image_nygv: Optional[str] = None

    cost_allocation_per: Optional[Decimal] = None

    process_loss_per: Optional[Decimal] = None

    cost: Optional[Decimal] = None

    base_cost: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None





class BomSecondaryItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    rate: Optional[Decimal] = None

    is_legacy: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    secondary_item_type: Optional[BomSecondaryItemSecondaryItemType] = None

    uom_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    image: Optional[str] = None

    description: Optional[str] = None

    image_nygv: Optional[str] = None

    cost_allocation_per: Optional[Decimal] = None

    process_loss_per: Optional[Decimal] = None

    cost: Optional[Decimal] = None

    base_cost: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None





BomSecondaryItemListResponse = Page[BomSecondaryItemRead]

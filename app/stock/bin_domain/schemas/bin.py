"""Pydantic v2 schemas for Bin."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BinCreate",

    "BinUpdate",

    "BinRead",

    "BinListResponse",

]





class BinBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    warehouse_id: uuid.UUID

    item_code_id: uuid.UUID

    reserved_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    indented_qty: Optional[Decimal] = None

    planned_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    reserved_qty_for_production: Optional[Decimal] = None

    reserved_qty_for_sub_contract: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    company: Optional[str] = None

    valuation_rate: Optional[Decimal] = None

    stock_value: Optional[Decimal] = None

    reserved_qty_for_production_plan: Optional[Decimal] = None

    reserved_stock: Optional[Decimal] = None





class BinCreate(BinBase):

    pass





class BinUpdate(InputSchema):

    """A partial update."""



    warehouse_id: Optional[uuid.UUID] = None

    item_code_id: Optional[uuid.UUID] = None

    reserved_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    indented_qty: Optional[Decimal] = None

    planned_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    reserved_qty_for_production: Optional[Decimal] = None

    reserved_qty_for_sub_contract: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    company: Optional[str] = None

    valuation_rate: Optional[Decimal] = None

    stock_value: Optional[Decimal] = None

    reserved_qty_for_production_plan: Optional[Decimal] = None

    reserved_stock: Optional[Decimal] = None





class BinRead(ReadSchema):

    id: uuid.UUID

    name: str

    warehouse_id: Optional[uuid.UUID] = None

    item_code_id: Optional[uuid.UUID] = None

    reserved_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    indented_qty: Optional[Decimal] = None

    planned_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    reserved_qty_for_production: Optional[Decimal] = None

    reserved_qty_for_sub_contract: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    company: Optional[str] = None

    valuation_rate: Optional[Decimal] = None

    stock_value: Optional[Decimal] = None

    reserved_qty_for_production_plan: Optional[Decimal] = None

    reserved_stock: Optional[Decimal] = None





BinListResponse = Page[BinRead]

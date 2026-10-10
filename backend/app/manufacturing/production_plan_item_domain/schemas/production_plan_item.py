"""Pydantic v2 schemas for ProductionPlanItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProductionPlanItemCreate",

    "ProductionPlanItemRead",

    "ProductionPlanItemListResponse",

]





class ProductionPlanItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    include_exploded_items: Optional[bool] = None

    item_code_id: uuid.UUID

    bom_no_id: uuid.UUID

    planned_qty: Decimal

    stock_uom_id: uuid.UUID

    warehouse_id: Optional[uuid.UUID] = None

    planned_start_date: dt.datetime

    pending_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    description: Optional[str] = None

    produced_qty: Optional[Decimal] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    product_bundle_item_id: Optional[uuid.UUID] = None

    item_reference: Optional[str] = None

    temporary_name: Optional[str] = None





class ProductionPlanItemCreate(ProductionPlanItemBase):

    pass





class ProductionPlanItemUpdate(InputSchema):

    """A partial update."""



    include_exploded_items: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None

    bom_no_id: Optional[uuid.UUID] = None

    planned_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    planned_start_date: Optional[dt.datetime] = None

    pending_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    description: Optional[str] = None

    produced_qty: Optional[Decimal] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    product_bundle_item_id: Optional[uuid.UUID] = None

    item_reference: Optional[str] = None

    temporary_name: Optional[str] = None





class ProductionPlanItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    include_exploded_items: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None

    bom_no_id: Optional[uuid.UUID] = None

    planned_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    planned_start_date: Optional[dt.datetime] = None

    pending_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    description: Optional[str] = None

    produced_qty: Optional[Decimal] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    product_bundle_item_id: Optional[uuid.UUID] = None

    item_reference: Optional[str] = None

    temporary_name: Optional[str] = None





ProductionPlanItemListResponse = Page[ProductionPlanItemRead]

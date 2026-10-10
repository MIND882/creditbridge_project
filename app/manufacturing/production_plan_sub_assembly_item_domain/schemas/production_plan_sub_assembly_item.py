"""Pydantic v2 schemas for ProductionPlanSubAssemblyItem."""





from __future__ import annotations

from app.manufacturing.production_plan_sub_assembly_item_domain.models.production_plan_sub_assembly_item import (

    ProductionPlanSubAssemblyItemTypeOfManufacturing,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProductionPlanSubAssemblyItemCreate",

    "ProductionPlanSubAssemblyItemRead",

    "ProductionPlanSubAssemblyItemListResponse",

]





class ProductionPlanSubAssemblyItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    production_item_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    parent_item_code_id: Optional[uuid.UUID] = None

    bom_no_id: Optional[uuid.UUID] = None

    bom_level: Optional[int] = None

    type_of_manufacturing: Optional[ProductionPlanSubAssemblyItemTypeOfManufacturing] = None

    required_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    qty: Optional[Decimal] = None

    supplier_id: Optional[uuid.UUID] = None

    purchase_order_id: Optional[uuid.UUID] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    production_plan_item: Optional[str] = None

    wo_produced_qty: Optional[Decimal] = None

    stock_reserved_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    received_qty: Optional[Decimal] = None

    indent: Optional[int] = None

    schedule_date: Optional[dt.datetime] = None

    uom_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    actual_qty: Optional[Decimal] = None

    description: Optional[str] = None





class ProductionPlanSubAssemblyItemCreate(ProductionPlanSubAssemblyItemBase):

    pass





class ProductionPlanSubAssemblyItemUpdate(InputSchema):

    """A partial update."""



    production_item_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    parent_item_code_id: Optional[uuid.UUID] = None

    bom_no_id: Optional[uuid.UUID] = None

    bom_level: Optional[int] = None

    type_of_manufacturing: Optional[ProductionPlanSubAssemblyItemTypeOfManufacturing] = None

    required_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    qty: Optional[Decimal] = None

    supplier_id: Optional[uuid.UUID] = None

    purchase_order_id: Optional[uuid.UUID] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    production_plan_item: Optional[str] = None

    wo_produced_qty: Optional[Decimal] = None

    stock_reserved_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    received_qty: Optional[Decimal] = None

    indent: Optional[int] = None

    schedule_date: Optional[dt.datetime] = None

    uom_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    actual_qty: Optional[Decimal] = None

    description: Optional[str] = None





class ProductionPlanSubAssemblyItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    production_item_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    fg_warehouse_id: Optional[uuid.UUID] = None

    parent_item_code_id: Optional[uuid.UUID] = None

    bom_no_id: Optional[uuid.UUID] = None

    bom_level: Optional[int] = None

    type_of_manufacturing: Optional[ProductionPlanSubAssemblyItemTypeOfManufacturing] = None

    required_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    qty: Optional[Decimal] = None

    supplier_id: Optional[uuid.UUID] = None

    purchase_order_id: Optional[uuid.UUID] = None

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_item: Optional[str] = None

    production_plan_item: Optional[str] = None

    wo_produced_qty: Optional[Decimal] = None

    stock_reserved_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    received_qty: Optional[Decimal] = None

    indent: Optional[int] = None

    schedule_date: Optional[dt.datetime] = None

    uom_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    actual_qty: Optional[Decimal] = None

    description: Optional[str] = None





ProductionPlanSubAssemblyItemListResponse = Page[ProductionPlanSubAssemblyItemRead]

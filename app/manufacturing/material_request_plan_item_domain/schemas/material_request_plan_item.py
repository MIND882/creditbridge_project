"""Pydantic v2 schemas for MaterialRequestPlanItem."""





from __future__ import annotations

from app.manufacturing.material_request_plan_item_domain.models.material_request_plan_item import (

    MaterialRequestPlanItemMaterialRequestType,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "MaterialRequestPlanItemCreate",

    "MaterialRequestPlanItemRead",

    "MaterialRequestPlanItemListResponse",

]





class MaterialRequestPlanItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    from_warehouse_id: Optional[uuid.UUID] = None

    warehouse_id: uuid.UUID

    material_request_type: Optional[MaterialRequestPlanItemMaterialRequestType] = None

    item_name: Optional[str] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    from_bom_id: Optional[uuid.UUID] = None

    main_item_code_id: Optional[uuid.UUID] = None

    required_bom_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    quantity: Decimal

    stock_reserved_qty: Optional[Decimal] = None

    schedule_date: Optional[dt.date] = None

    description: Optional[str] = None

    min_order_qty: Optional[Decimal] = None

    sales_order_id: Optional[uuid.UUID] = None

    sub_assembly_item_reference: Optional[str] = None

    actual_qty: Optional[Decimal] = None

    requested_qty: Optional[Decimal] = None

    reserved_qty_for_production: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    safety_stock: Optional[Decimal] = None





class MaterialRequestPlanItemCreate(MaterialRequestPlanItemBase):

    pass





class MaterialRequestPlanItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    material_request_type: Optional[MaterialRequestPlanItemMaterialRequestType] = None

    item_name: Optional[str] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    from_bom_id: Optional[uuid.UUID] = None

    main_item_code_id: Optional[uuid.UUID] = None

    required_bom_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    quantity: Optional[Decimal] = None

    stock_reserved_qty: Optional[Decimal] = None

    schedule_date: Optional[dt.date] = None

    description: Optional[str] = None

    min_order_qty: Optional[Decimal] = None

    sales_order_id: Optional[uuid.UUID] = None

    sub_assembly_item_reference: Optional[str] = None

    actual_qty: Optional[Decimal] = None

    requested_qty: Optional[Decimal] = None

    reserved_qty_for_production: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    safety_stock: Optional[Decimal] = None





class MaterialRequestPlanItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    material_request_type: Optional[MaterialRequestPlanItemMaterialRequestType] = None

    item_name: Optional[str] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    from_bom_id: Optional[uuid.UUID] = None

    main_item_code_id: Optional[uuid.UUID] = None

    required_bom_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    quantity: Optional[Decimal] = None

    stock_reserved_qty: Optional[Decimal] = None

    schedule_date: Optional[dt.date] = None

    description: Optional[str] = None

    min_order_qty: Optional[Decimal] = None

    sales_order_id: Optional[uuid.UUID] = None

    sub_assembly_item_reference: Optional[str] = None

    actual_qty: Optional[Decimal] = None

    requested_qty: Optional[Decimal] = None

    reserved_qty_for_production: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    safety_stock: Optional[Decimal] = None





MaterialRequestPlanItemListResponse = Page[MaterialRequestPlanItemRead]

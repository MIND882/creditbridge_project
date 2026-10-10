"""Pydantic v2 schemas for MaterialRequestItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "MaterialRequestItemCreate",

    "MaterialRequestItemRead",

    "MaterialRequestItemListResponse",

]





class MaterialRequestItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    qty: Decimal

    uom_id: uuid.UUID

    conversion_factor: Decimal

    stock_uom_id: uuid.UUID

    warehouse_id: Optional[uuid.UUID] = None

    schedule_date: dt.date

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    lead_time_date: Optional[dt.date] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    project: Optional[str] = None

    production_plan: Optional[str] = None

    material_request_plan_item: Optional[str] = None

    min_order_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    received_qty: Optional[Decimal] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    bom_no: Optional[str] = None

    job_card_item: Optional[str] = None

    wip_composite_asset: Optional[str] = None

    price_list_rate: Optional[Decimal] = None

    reorder_level: Optional[Decimal] = None

    reorder_qty: Optional[Decimal] = None

    projected_on_hand: Optional[Decimal] = None

    picked_qty: Optional[Decimal] = None

    packed_item: Optional[str] = None





class MaterialRequestItemCreate(MaterialRequestItemBase):

    pass





class MaterialRequestItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    schedule_date: Optional[dt.date] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    lead_time_date: Optional[dt.date] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    project: Optional[str] = None

    production_plan: Optional[str] = None

    material_request_plan_item: Optional[str] = None

    min_order_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    received_qty: Optional[Decimal] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    bom_no: Optional[str] = None

    job_card_item: Optional[str] = None

    wip_composite_asset: Optional[str] = None

    price_list_rate: Optional[Decimal] = None

    reorder_level: Optional[Decimal] = None

    reorder_qty: Optional[Decimal] = None

    projected_on_hand: Optional[Decimal] = None

    picked_qty: Optional[Decimal] = None

    packed_item: Optional[str] = None





class MaterialRequestItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    schedule_date: Optional[dt.date] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    lead_time_date: Optional[dt.date] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    project: Optional[str] = None

    production_plan: Optional[str] = None

    material_request_plan_item: Optional[str] = None

    min_order_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    received_qty: Optional[Decimal] = None

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    from_warehouse_id: Optional[uuid.UUID] = None

    bom_no: Optional[str] = None

    job_card_item: Optional[str] = None

    wip_composite_asset: Optional[str] = None

    price_list_rate: Optional[Decimal] = None

    reorder_level: Optional[Decimal] = None

    reorder_qty: Optional[Decimal] = None

    projected_on_hand: Optional[Decimal] = None

    picked_qty: Optional[Decimal] = None

    packed_item: Optional[str] = None





MaterialRequestItemListResponse = Page[MaterialRequestItemRead]

"""Pydantic v2 schemas for RequestForQuotationItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "RequestForQuotationItemCreate",

    "RequestForQuotationItemRead",

    "RequestForQuotationItemListResponse",

]





class RequestForQuotationItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    supplier_part_no: Optional[str] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Decimal

    schedule_date: dt.date

    uom_id: uuid.UUID

    warehouse_id: Optional[uuid.UUID] = None

    project_name: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    stock_uom_id: uuid.UUID

    conversion_factor: Decimal

    stock_qty: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None





class RequestForQuotationItemCreate(RequestForQuotationItemBase):

    pass





class RequestForQuotationItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    supplier_part_no: Optional[str] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    schedule_date: Optional[dt.date] = None

    uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    project_name: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    stock_uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None





class RequestForQuotationItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    supplier_part_no: Optional[str] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None

    image_view: Optional[str] = None

    qty: Optional[Decimal] = None

    schedule_date: Optional[dt.date] = None

    uom_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    project_name: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    brand_id: Optional[uuid.UUID] = None

    item_group_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    stock_uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None





RequestForQuotationItemListResponse = Page[RequestForQuotationItemRead]

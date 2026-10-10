"""Pydantic v2 schemas for WorkOrderItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WorkOrderItemCreate",

    "WorkOrderItemRead",

    "WorkOrderItemListResponse",

]





class WorkOrderItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    operation_id: Optional[uuid.UUID] = None

    item_code_id: Optional[uuid.UUID] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    operation_row_id: Optional[int] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    allow_alternative_item: Optional[bool] = None

    include_item_in_manufacturing: Optional[bool] = None

    required_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    consumed_qty: Optional[Decimal] = None

    returned_qty: Optional[Decimal] = None

    available_qty_at_source_warehouse: Optional[Decimal] = None

    available_qty_at_wip_warehouse: Optional[Decimal] = None

    stock_reserved_qty: Optional[Decimal] = None

    is_additional_item: Optional[bool] = None

    is_customer_provided_item: Optional[bool] = None

    voucher_detail_reference: Optional[str] = None





class WorkOrderItemCreate(WorkOrderItemBase):

    pass





class WorkOrderItemUpdate(InputSchema):

    """A partial update."""



    operation_id: Optional[uuid.UUID] = None

    item_code_id: Optional[uuid.UUID] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    operation_row_id: Optional[int] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    allow_alternative_item: Optional[bool] = None

    include_item_in_manufacturing: Optional[bool] = None

    required_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    consumed_qty: Optional[Decimal] = None

    returned_qty: Optional[Decimal] = None

    available_qty_at_source_warehouse: Optional[Decimal] = None

    available_qty_at_wip_warehouse: Optional[Decimal] = None

    stock_reserved_qty: Optional[Decimal] = None

    is_additional_item: Optional[bool] = None

    is_customer_provided_item: Optional[bool] = None

    voucher_detail_reference: Optional[str] = None





class WorkOrderItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    operation_id: Optional[uuid.UUID] = None

    item_code_id: Optional[uuid.UUID] = None

    source_warehouse_id: Optional[uuid.UUID] = None

    operation_row_id: Optional[int] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    allow_alternative_item: Optional[bool] = None

    include_item_in_manufacturing: Optional[bool] = None

    required_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    consumed_qty: Optional[Decimal] = None

    returned_qty: Optional[Decimal] = None

    available_qty_at_source_warehouse: Optional[Decimal] = None

    available_qty_at_wip_warehouse: Optional[Decimal] = None

    stock_reserved_qty: Optional[Decimal] = None

    is_additional_item: Optional[bool] = None

    is_customer_provided_item: Optional[bool] = None

    voucher_detail_reference: Optional[str] = None





WorkOrderItemListResponse = Page[WorkOrderItemRead]

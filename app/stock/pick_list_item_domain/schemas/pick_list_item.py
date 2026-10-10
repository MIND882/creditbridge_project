"""Pydantic v2 schemas for PickListItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PickListItemCreate",

    "PickListItemRead",

    "PickListItemListResponse",

]





class PickListItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    qty: Decimal

    picked_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    item_code_id: uuid.UUID

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    item_group: Optional[str] = None

    product_bundle_item: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    stock_reserved_qty: Optional[Decimal] = None

    use_serial_batch_fields: Optional[bool] = None

    delivered_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None





class PickListItemCreate(PickListItemBase):

    pass





class PickListItemUpdate(InputSchema):

    """A partial update."""



    qty: Optional[Decimal] = None

    picked_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    item_code_id: Optional[uuid.UUID] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    item_group: Optional[str] = None

    product_bundle_item: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    stock_reserved_qty: Optional[Decimal] = None

    use_serial_batch_fields: Optional[bool] = None

    delivered_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None





class PickListItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    qty: Optional[Decimal] = None

    picked_qty: Optional[Decimal] = None

    warehouse_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    stock_uom_id: Optional[uuid.UUID] = None

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None

    stock_qty: Optional[Decimal] = None

    item_code_id: Optional[uuid.UUID] = None

    sales_order: Optional[str] = None

    sales_order_item: Optional[str] = None

    material_request_id: Optional[uuid.UUID] = None

    material_request_item: Optional[str] = None

    item_group: Optional[str] = None

    product_bundle_item: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    stock_reserved_qty: Optional[Decimal] = None

    use_serial_batch_fields: Optional[bool] = None

    delivered_qty: Optional[Decimal] = None

    transferred_qty: Optional[Decimal] = None

    actual_qty: Optional[Decimal] = None

    company_total_stock: Optional[Decimal] = None





PickListItemListResponse = Page[PickListItemRead]

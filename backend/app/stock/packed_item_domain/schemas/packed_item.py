"""Pydantic v2 schemas for PackedItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PackedItemCreate",

    "PackedItemRead",

    "PackedItemListResponse",

]





class PackedItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parent_item_id: Optional[uuid.UUID] = None

    item_code_id: Optional[uuid.UUID] = None

    product_bundle: Optional[str] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    target_warehouse_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    actual_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    prevdoc_doctype: Optional[str] = None

    parent_detail_docname: Optional[str] = None

    actual_batch_qty: Optional[Decimal] = None

    incoming_rate: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    picked_qty: Optional[Decimal] = None

    packed_qty: Optional[Decimal] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    delivered_by_supplier: Optional[bool] = None

    requested_qty: Optional[Decimal] = None

    reserve_stock: Optional[bool] = None





class PackedItemCreate(PackedItemBase):

    pass





class PackedItemUpdate(InputSchema):

    """A partial update."""



    parent_item_id: Optional[uuid.UUID] = None

    item_code_id: Optional[uuid.UUID] = None

    product_bundle: Optional[str] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    target_warehouse_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    actual_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    prevdoc_doctype: Optional[str] = None

    parent_detail_docname: Optional[str] = None

    actual_batch_qty: Optional[Decimal] = None

    incoming_rate: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    picked_qty: Optional[Decimal] = None

    packed_qty: Optional[Decimal] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    delivered_by_supplier: Optional[bool] = None

    requested_qty: Optional[Decimal] = None

    reserve_stock: Optional[bool] = None





class PackedItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    parent_item_id: Optional[uuid.UUID] = None

    item_code_id: Optional[uuid.UUID] = None

    product_bundle: Optional[str] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    target_warehouse_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    serial_no: Optional[str] = None

    batch_no_id: Optional[uuid.UUID] = None

    actual_qty: Optional[Decimal] = None

    projected_qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    page_break: Optional[bool] = None

    prevdoc_doctype: Optional[str] = None

    parent_detail_docname: Optional[str] = None

    actual_batch_qty: Optional[Decimal] = None

    incoming_rate: Optional[Decimal] = None

    conversion_factor: Optional[Decimal] = None

    rate: Optional[Decimal] = None

    ordered_qty: Optional[Decimal] = None

    picked_qty: Optional[Decimal] = None

    packed_qty: Optional[Decimal] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None

    use_serial_batch_fields: Optional[bool] = None

    delivered_by_supplier: Optional[bool] = None

    requested_qty: Optional[Decimal] = None

    reserve_stock: Optional[bool] = None





PackedItemListResponse = Page[PackedItemRead]

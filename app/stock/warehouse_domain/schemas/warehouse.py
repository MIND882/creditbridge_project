"""Pydantic v2 schemas for Warehouse."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WarehouseCreate",

    "WarehouseUpdate",

    "WarehouseRead",

    "WarehouseListResponse",

]





class WarehouseBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    warehouse_name: str

    is_group: Optional[bool] = None

    company: str

    disabled: Optional[bool] = None

    account_id: Optional[uuid.UUID] = None

    email_id: Optional[str] = None

    phone_no: Optional[str] = None

    mobile_no: Optional[str] = None

    address_line_1: Optional[str] = None

    address_line_2: Optional[str] = None

    city: Optional[str] = None

    state: Optional[str] = None

    pin: Optional[str] = None

    parent_warehouse_id: Optional[uuid.UUID] = None

    lft: Optional[int] = None

    rgt: Optional[int] = None

    old_parent_id: Optional[uuid.UUID] = None

    warehouse_type_id: Optional[uuid.UUID] = None

    default_in_transit_warehouse_id: Optional[uuid.UUID] = None

    is_rejected_warehouse: Optional[bool] = None

    customer: Optional[str] = None





class WarehouseCreate(WarehouseBase):

    pass





class WarehouseUpdate(InputSchema):

    """A partial update."""



    warehouse_name: Optional[str] = None

    is_group: Optional[bool] = None

    company: Optional[str] = None

    disabled: Optional[bool] = None

    account_id: Optional[uuid.UUID] = None

    email_id: Optional[str] = None

    phone_no: Optional[str] = None

    mobile_no: Optional[str] = None

    address_line_1: Optional[str] = None

    address_line_2: Optional[str] = None

    city: Optional[str] = None

    state: Optional[str] = None

    pin: Optional[str] = None

    parent_warehouse_id: Optional[uuid.UUID] = None

    lft: Optional[int] = None

    rgt: Optional[int] = None

    old_parent_id: Optional[uuid.UUID] = None

    warehouse_type_id: Optional[uuid.UUID] = None

    default_in_transit_warehouse_id: Optional[uuid.UUID] = None

    is_rejected_warehouse: Optional[bool] = None

    customer: Optional[str] = None





class WarehouseRead(ReadSchema):

    id: uuid.UUID

    name: str

    warehouse_name: str

    is_group: Optional[bool] = None

    company: str

    disabled: Optional[bool] = None

    account_id: Optional[uuid.UUID] = None

    email_id: Optional[str] = None

    phone_no: Optional[str] = None

    mobile_no: Optional[str] = None

    address_line_1: Optional[str] = None

    address_line_2: Optional[str] = None

    city: Optional[str] = None

    state: Optional[str] = None

    pin: Optional[str] = None

    parent_warehouse_id: Optional[uuid.UUID] = None

    lft: Optional[int] = None

    rgt: Optional[int] = None

    old_parent_id: Optional[uuid.UUID] = None

    warehouse_type_id: Optional[uuid.UUID] = None

    default_in_transit_warehouse_id: Optional[uuid.UUID] = None

    is_rejected_warehouse: Optional[bool] = None

    customer: Optional[str] = None





WarehouseListResponse = Page[WarehouseRead]

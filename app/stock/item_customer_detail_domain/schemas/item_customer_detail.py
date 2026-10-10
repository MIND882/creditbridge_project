"""Pydantic v2 schemas for ItemCustomerDetail."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemCustomerDetailCreate",

    "ItemCustomerDetailRead",

    "ItemCustomerDetailListResponse",

]





class ItemCustomerDetailBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    customer_name: Optional[str] = None

    customer_group: Optional[str] = None

    ref_code: str





class ItemCustomerDetailCreate(ItemCustomerDetailBase):

    pass





class ItemCustomerDetailUpdate(InputSchema):

    """A partial update."""



    customer_name: Optional[str] = None

    customer_group: Optional[str] = None

    ref_code: Optional[str] = None





class ItemCustomerDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    customer_name: Optional[str] = None

    customer_group: Optional[str] = None

    ref_code: str





ItemCustomerDetailListResponse = Page[ItemCustomerDetailRead]

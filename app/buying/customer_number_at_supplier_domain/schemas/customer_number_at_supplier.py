"""Pydantic v2 schemas for CustomerNumberAtSupplier."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CustomerNumberAtSupplierCreate",

    "CustomerNumberAtSupplierRead",

    "CustomerNumberAtSupplierListResponse",

]





class CustomerNumberAtSupplierBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    company: Optional[str] = None

    customer_number: Optional[str] = None





class CustomerNumberAtSupplierCreate(CustomerNumberAtSupplierBase):

    pass





class CustomerNumberAtSupplierUpdate(InputSchema):

    """A partial update."""



    company: Optional[str] = None

    customer_number: Optional[str] = None





class CustomerNumberAtSupplierRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    company: Optional[str] = None

    customer_number: Optional[str] = None





CustomerNumberAtSupplierListResponse = Page[CustomerNumberAtSupplierRead]

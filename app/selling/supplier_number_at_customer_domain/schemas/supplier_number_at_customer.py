"""Pydantic v2 schemas for SupplierNumberAtCustomer."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierNumberAtCustomerCreate",

    "SupplierNumberAtCustomerRead",

    "SupplierNumberAtCustomerListResponse",

]





class SupplierNumberAtCustomerBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    company: Optional[str] = None

    supplier_number: Optional[str] = None





class SupplierNumberAtCustomerCreate(SupplierNumberAtCustomerBase):

    pass





class SupplierNumberAtCustomerUpdate(InputSchema):

    """A partial update."""



    company: Optional[str] = None

    supplier_number: Optional[str] = None





class SupplierNumberAtCustomerRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    company: Optional[str] = None

    supplier_number: Optional[str] = None





SupplierNumberAtCustomerListResponse = Page[SupplierNumberAtCustomerRead]

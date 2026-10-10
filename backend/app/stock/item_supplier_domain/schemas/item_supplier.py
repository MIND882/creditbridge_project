"""Pydantic v2 schemas for ItemSupplier."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemSupplierCreate",

    "ItemSupplierRead",

    "ItemSupplierListResponse",

]





class ItemSupplierBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    supplier: str

    supplier_part_no: Optional[str] = None





class ItemSupplierCreate(ItemSupplierBase):

    pass





class ItemSupplierUpdate(InputSchema):

    """A partial update."""



    supplier: Optional[str] = None

    supplier_part_no: Optional[str] = None





class ItemSupplierRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    supplier: str

    supplier_part_no: Optional[str] = None





ItemSupplierListResponse = Page[ItemSupplierRead]

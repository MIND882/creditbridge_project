"""Pydantic v2 schemas for SupplierGroupItem."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierGroupItemCreate",

    "SupplierGroupItemRead",

    "SupplierGroupItemListResponse",

]





class SupplierGroupItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    supplier_group: Optional[str] = None





class SupplierGroupItemCreate(SupplierGroupItemBase):

    """Accepted only nested inside the parent payload."""

    pass





class SupplierGroupItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    supplier_group: Optional[str] = None





SupplierGroupItemListResponse = Page[SupplierGroupItemRead]

"""Pydantic v2 schemas for SupplierItem."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierItemCreate",

    "SupplierItemRead",

    "SupplierItemListResponse",

]





class SupplierItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    supplier: Optional[str] = None





class SupplierItemCreate(SupplierItemBase):

    """Accepted only nested inside the parent payload."""

    pass





class SupplierItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    supplier: Optional[str] = None





SupplierItemListResponse = Page[SupplierItemRead]

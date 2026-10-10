"""Pydantic v2 schemas for CustomerItem."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CustomerItemCreate",

    "CustomerItemRead",

    "CustomerItemListResponse",

]





class CustomerItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    customer: Optional[str] = None





class CustomerItemCreate(CustomerItemBase):

    """Accepted only nested inside the parent payload."""

    pass





class CustomerItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    customer: Optional[str] = None





CustomerItemListResponse = Page[CustomerItemRead]

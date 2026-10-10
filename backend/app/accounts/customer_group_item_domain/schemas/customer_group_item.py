"""Pydantic v2 schemas for CustomerGroupItem."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CustomerGroupItemCreate",

    "CustomerGroupItemRead",

    "CustomerGroupItemListResponse",

]





class CustomerGroupItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    customer_group: Optional[str] = None





class CustomerGroupItemCreate(CustomerGroupItemBase):

    """Accepted only nested inside the parent payload."""

    pass





class CustomerGroupItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    customer_group: Optional[str] = None





CustomerGroupItemListResponse = Page[CustomerGroupItemRead]

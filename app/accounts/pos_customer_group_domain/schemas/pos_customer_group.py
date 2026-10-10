"""Pydantic v2 schemas for POSCustomerGroup."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "POSCustomerGroupCreate",

    "POSCustomerGroupRead",

    "POSCustomerGroupListResponse",

]





class POSCustomerGroupBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    customer_group: str





class POSCustomerGroupCreate(POSCustomerGroupBase):

    """Accepted only nested inside the parent payload."""

    pass





class POSCustomerGroupRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    customer_group: str





POSCustomerGroupListResponse = Page[POSCustomerGroupRead]

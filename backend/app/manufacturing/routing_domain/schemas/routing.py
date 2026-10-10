"""Pydantic v2 schemas for Routing."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "RoutingCreate",

    "RoutingUpdate",

    "RoutingRead",

    "RoutingListResponse",

]





class RoutingBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    routing_name: Optional[str] = None

    disabled: Optional[bool] = None





class RoutingCreate(RoutingBase):

    pass





class RoutingUpdate(InputSchema):

    """A partial update."""



    routing_name: Optional[str] = None

    disabled: Optional[bool] = None





class RoutingRead(ReadSchema):

    id: uuid.UUID

    name: str

    routing_name: Optional[str] = None

    disabled: Optional[bool] = None





RoutingListResponse = Page[RoutingRead]

"""Pydantic v2 schemas for POSField."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "POSFieldCreate",

    "POSFieldRead",

    "POSFieldListResponse",

]





class POSFieldBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    fieldname: Optional[str] = None

    fieldtype: Optional[str] = None

    label: Optional[str] = None

    options: Optional[str] = None

    reqd: Optional[bool] = None

    read_only: Optional[bool] = None

    default_value: Optional[str] = None





class POSFieldCreate(POSFieldBase):

    """Accepted only nested inside the parent payload."""

    pass





class POSFieldRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    fieldname: Optional[str] = None

    fieldtype: Optional[str] = None

    label: Optional[str] = None

    options: Optional[str] = None

    reqd: bool

    read_only: bool

    default_value: Optional[str] = None





POSFieldListResponse = Page[POSFieldRead]

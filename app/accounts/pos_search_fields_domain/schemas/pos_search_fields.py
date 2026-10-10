"""Pydantic v2 schemas for POSSearchFields."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "POSSearchFieldsCreate",

    "POSSearchFieldsRead",

    "POSSearchFieldsListResponse",

]





class POSSearchFieldsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    fieldname: Optional[str] = None

    field: Optional[str] = None





class POSSearchFieldsCreate(POSSearchFieldsBase):

    """Accepted only nested inside the parent payload."""

    pass





class POSSearchFieldsRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    fieldname: Optional[str] = None

    field: Optional[str] = None





POSSearchFieldsListResponse = Page[POSSearchFieldsRead]

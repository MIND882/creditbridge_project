"""Pydantic v2 schemas for ClosedDocument."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ClosedDocumentCreate",

    "ClosedDocumentRead",

    "ClosedDocumentListResponse",

]





class ClosedDocumentBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    document_type: str

    closed: Optional[bool] = None





class ClosedDocumentCreate(ClosedDocumentBase):

    """Accepted only nested inside the parent payload."""

    pass





class ClosedDocumentRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    document_type: str

    closed: bool





ClosedDocumentListResponse = Page[ClosedDocumentRead]

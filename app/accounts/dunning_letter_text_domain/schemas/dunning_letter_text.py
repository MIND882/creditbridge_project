"""Pydantic v2 schemas for DunningLetterText (child table, read-only API)."""



from __future__ import annotations



import uuid

from typing import Optional



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "DunningLetterTextCreate",

    "DunningLetterTextRead",

    "DunningLetterTextListResponse",

]





class DunningLetterTextCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    language: Optional[str] = None

    is_default_language: Optional[bool] = False

    body_text: Optional[str] = None

    closing_text: Optional[str] = None





class DunningLetterTextRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    language: Optional[str] = None

    is_default_language: bool

    body_text: Optional[str] = None

    closing_text: Optional[str] = None





DunningLetterTextListResponse = Page[DunningLetterTextRead]

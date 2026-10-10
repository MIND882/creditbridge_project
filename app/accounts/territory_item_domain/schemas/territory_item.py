"""Pydantic v2 schemas for TerritoryItem."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "TerritoryItemCreate",

    "TerritoryItemRead",

    "TerritoryItemListResponse",

]





class TerritoryItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    territory: Optional[str] = None





class TerritoryItemCreate(TerritoryItemBase):

    """Accepted only nested inside the parent payload."""

    pass





class TerritoryItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    territory: Optional[str] = None





TerritoryItemListResponse = Page[TerritoryItemRead]

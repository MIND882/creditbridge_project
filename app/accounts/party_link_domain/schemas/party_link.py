"""Pydantic v2 schemas for PartyLink."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PartyLinkCreate",

    "PartyLinkUpdate",

    "PartyLinkRead",

    "PartyLinkListResponse",

]





class PartyLinkBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    primary_role: str

    secondary_role: Optional[str] = None

    primary_party: Optional[str] = None

    secondary_party: Optional[str] = None





class PartyLinkCreate(PartyLinkBase):

    pass





class PartyLinkUpdate(InputSchema):

    """A partial update."""



    primary_role: Optional[str] = None

    secondary_role: Optional[str] = None

    primary_party: Optional[str] = None

    secondary_party: Optional[str] = None





class PartyLinkRead(ReadSchema):

    id: uuid.UUID

    name: str

    primary_role: str

    secondary_role: Optional[str] = None

    primary_party: Optional[str] = None

    secondary_party: Optional[str] = None





PartyLinkListResponse = Page[PartyLinkRead]

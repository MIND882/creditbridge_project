"""Pydantic v2 schemas for PartySpecificItem."""





from __future__ import annotations

from app.selling.party_specific_item_domain.models.party_specific_item import (

    PartySpecificItemPartyType,

    PartySpecificItemRestrictBasedOn,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PartySpecificItemCreate",

    "PartySpecificItemUpdate",

    "PartySpecificItemRead",

    "PartySpecificItemListResponse",

]





class PartySpecificItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    party_type: PartySpecificItemPartyType

    party: str

    restrict_based_on: PartySpecificItemRestrictBasedOn

    based_on_value: str





class PartySpecificItemCreate(PartySpecificItemBase):

    pass





class PartySpecificItemUpdate(InputSchema):

    """A partial update."""



    party_type: Optional[PartySpecificItemPartyType] = None

    party: Optional[str] = None

    restrict_based_on: Optional[PartySpecificItemRestrictBasedOn] = None

    based_on_value: Optional[str] = None





class PartySpecificItemRead(ReadSchema):

    id: uuid.UUID

    name: str

    party_type: Optional[PartySpecificItemPartyType] = None

    party: str

    restrict_based_on: Optional[PartySpecificItemRestrictBasedOn] = None

    based_on_value: str





PartySpecificItemListResponse = Page[PartySpecificItemRead]

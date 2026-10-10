"""Pydantic v2 schemas for LoyaltyProgramCollection."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LoyaltyProgramCollectionCreate",

    "LoyaltyProgramCollectionRead",

    "LoyaltyProgramCollectionListResponse",

]





class LoyaltyProgramCollectionBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    tier_name: str

    min_spent: Optional[Decimal] = None

    collection_factor: Optional[Decimal] = None





class LoyaltyProgramCollectionCreate(LoyaltyProgramCollectionBase):

    """Accepted only nested inside the parent payload."""

    pass





class LoyaltyProgramCollectionRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    tier_name: str

    min_spent: Optional[Decimal] = None

    collection_factor: Decimal





LoyaltyProgramCollectionListResponse = Page[LoyaltyProgramCollectionRead]

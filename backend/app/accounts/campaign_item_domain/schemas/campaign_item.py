"""Pydantic v2 schemas for CampaignItem."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CampaignItemCreate",

    "CampaignItemRead",

    "CampaignItemListResponse",

]





class CampaignItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    campaign: Optional[str] = None





class CampaignItemCreate(CampaignItemBase):

    """Accepted only nested inside the parent payload."""

    pass





class CampaignItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    campaign: Optional[str] = None





CampaignItemListResponse = Page[CampaignItemRead]

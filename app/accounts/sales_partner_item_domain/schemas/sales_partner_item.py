"""Pydantic v2 schemas for SalesPartnerItem."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesPartnerItemCreate",

    "SalesPartnerItemRead",

    "SalesPartnerItemListResponse",

]





class SalesPartnerItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    sales_partner: Optional[str] = None





class SalesPartnerItemCreate(SalesPartnerItemBase):

    """Accepted only nested inside the parent payload."""

    pass





class SalesPartnerItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    sales_partner: Optional[str] = None





SalesPartnerItemListResponse = Page[SalesPartnerItemRead]

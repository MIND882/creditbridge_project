"""Pydantic v2 schemas for SalesPartnerType."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesPartnerTypeCreate",

    "SalesPartnerTypeUpdate",

    "SalesPartnerTypeRead",

    "SalesPartnerTypeListResponse",

]





class SalesPartnerTypeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    sales_partner_type: str





class SalesPartnerTypeCreate(SalesPartnerTypeBase):

    pass





class SalesPartnerTypeUpdate(InputSchema):

    """A partial update."""



    sales_partner_type: Optional[str] = None





class SalesPartnerTypeRead(ReadSchema):

    id: uuid.UUID

    name: str

    sales_partner_type: str





SalesPartnerTypeListResponse = Page[SalesPartnerTypeRead]

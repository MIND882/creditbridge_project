"""Pydantic v2 schemas for TaxWithholdingGroup."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "TaxWithholdingGroupCreate",

    "TaxWithholdingGroupUpdate",

    "TaxWithholdingGroupRead",

    "TaxWithholdingGroupListResponse",

]





class TaxWithholdingGroupBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    group_name: str





class TaxWithholdingGroupCreate(TaxWithholdingGroupBase):

    pass





class TaxWithholdingGroupUpdate(InputSchema):

    """A partial update."""



    group_name: Optional[str] = None





class TaxWithholdingGroupRead(ReadSchema):

    id: uuid.UUID

    name: str

    group_name: str





TaxWithholdingGroupListResponse = Page[TaxWithholdingGroupRead]

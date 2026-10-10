"""Pydantic v2 schemas for BomWebsiteOperation."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomWebsiteOperationCreate",

    "BomWebsiteOperationRead",

    "BomWebsiteOperationListResponse",

]





class BomWebsiteOperationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    operation_id: uuid.UUID

    workstation_id: Optional[uuid.UUID] = None

    time_in_mins: Decimal

    website_image: Optional[str] = None

    thumbnail: Optional[str] = None





class BomWebsiteOperationCreate(BomWebsiteOperationBase):

    pass





class BomWebsiteOperationUpdate(InputSchema):

    """A partial update."""



    operation_id: Optional[uuid.UUID] = None

    workstation_id: Optional[uuid.UUID] = None

    time_in_mins: Optional[Decimal] = None

    website_image: Optional[str] = None

    thumbnail: Optional[str] = None





class BomWebsiteOperationRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    operation_id: Optional[uuid.UUID] = None

    workstation_id: Optional[uuid.UUID] = None

    time_in_mins: Optional[Decimal] = None

    website_image: Optional[str] = None

    thumbnail: Optional[str] = None





BomWebsiteOperationListResponse = Page[BomWebsiteOperationRead]

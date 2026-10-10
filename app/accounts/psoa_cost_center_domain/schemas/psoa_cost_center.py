"""Pydantic v2 schemas for PsoaCostCenter."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PsoaCostCenterCreate",

    "PsoaCostCenterRead",

    "PsoaCostCenterListResponse",

]





class PsoaCostCenterBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    cost_center_name_id: uuid.UUID





class PsoaCostCenterCreate(PsoaCostCenterBase):

    """Accepted only nested inside the parent payload."""

    pass





class PsoaCostCenterRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    cost_center_name_id: uuid.UUID





PsoaCostCenterListResponse = Page[PsoaCostCenterRead]

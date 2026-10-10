"""Pydantic v2 schemas for PsoaProject."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PsoaProjectCreate",

    "PsoaProjectRead",

    "PsoaProjectListResponse",

]





class PsoaProjectBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    project_name: Optional[str] = None





class PsoaProjectCreate(PsoaProjectBase):

    """Accepted only nested inside the parent payload."""

    pass





class PsoaProjectRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    project_name: Optional[str] = None





PsoaProjectListResponse = Page[PsoaProjectRead]

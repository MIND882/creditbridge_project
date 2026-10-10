"""Pydantic v2 schemas for ProcessStatementOfAccountsCc."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProcessStatementOfAccountsCcCreate",

    "ProcessStatementOfAccountsCcRead",

    "ProcessStatementOfAccountsCcListResponse",

]





class ProcessStatementOfAccountsCcBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    cc: Optional[str] = None





class ProcessStatementOfAccountsCcCreate(ProcessStatementOfAccountsCcBase):

    """Accepted only nested inside the parent payload."""

    pass





class ProcessStatementOfAccountsCcRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    cc: Optional[str] = None





ProcessStatementOfAccountsCcListResponse = Page[ProcessStatementOfAccountsCcRead]

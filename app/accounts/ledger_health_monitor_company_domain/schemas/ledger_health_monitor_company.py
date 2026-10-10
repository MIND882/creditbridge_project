"""Pydantic v2 schemas for LedgerHealthMonitorCompany."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LedgerHealthMonitorCompanyCreate",

    "LedgerHealthMonitorCompanyRead",

    "LedgerHealthMonitorCompanyListResponse",

]





class LedgerHealthMonitorCompanyBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    pass





class LedgerHealthMonitorCompanyCreate(LedgerHealthMonitorCompanyBase):

    """Accepted only nested inside the parent payload."""

    pass





class LedgerHealthMonitorCompanyRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None





LedgerHealthMonitorCompanyListResponse = Page[LedgerHealthMonitorCompanyRead]

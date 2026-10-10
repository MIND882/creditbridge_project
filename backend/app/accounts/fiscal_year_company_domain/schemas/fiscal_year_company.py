"""Pydantic v2 schemas for FiscalYearCompany (child table, read-only API)."""



from __future__ import annotations



import uuid

from typing import Optional



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "FiscalYearCompanyCreate",

    "FiscalYearCompanyRead",

    "FiscalYearCompanyListResponse",

]





class FiscalYearCompanyCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    company: str





class FiscalYearCompanyRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    company: str





FiscalYearCompanyListResponse = Page[FiscalYearCompanyRead]

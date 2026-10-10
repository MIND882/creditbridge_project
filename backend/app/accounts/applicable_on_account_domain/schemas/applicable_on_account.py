"""Pydantic v2 schemas for Applicable On Account (a child table of Accounting Dimension Filter)."""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = ["ApplicableOnAccountCreate", "ApplicableOnAccountUpdate", "ApplicableOnAccountRead", "ApplicableOnAccountListResponse"]





class ApplicableOnAccountCreate(InputSchema):

    account_id: uuid.UUID

    is_mandatory: bool









class ApplicableOnAccountUpdate(InputSchema):

    account_id: Optional[uuid.UUID] = None

    is_mandatory: Optional[bool] = None









class ApplicableOnAccountRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    parent_id: Optional[uuid.UUID] = None

    idx: int

    account_id: uuid.UUID

    is_mandatory: bool

    created_at: datetime

    updated_at: datetime





ApplicableOnAccountListResponse = Page[ApplicableOnAccountRead]

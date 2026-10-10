"""Pydantic v2 schemas for Allowed Dimension (a child table of Accounting Dimension Filter)."""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = ["AllowedDimensionCreate", "AllowedDimensionUpdate", "AllowedDimensionRead", "AllowedDimensionListResponse"]





class AllowedDimensionCreate(InputSchema):

    accounting_dimension: Optional[Optional[str]] = None

    dimension_value: Optional[Optional[str]] = None









class AllowedDimensionUpdate(InputSchema):

    accounting_dimension: Optional[Optional[str]] = None

    dimension_value: Optional[Optional[str]] = None









class AllowedDimensionRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    parent_id: Optional[uuid.UUID] = None

    idx: int

    accounting_dimension: Optional[Optional[str]] = None

    dimension_value: Optional[Optional[str]] = None

    created_at: datetime

    updated_at: datetime





AllowedDimensionListResponse = Page[AllowedDimensionRead]

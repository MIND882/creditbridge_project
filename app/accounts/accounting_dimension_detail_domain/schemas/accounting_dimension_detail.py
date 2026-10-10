"""Pydantic v2 schemas for Accounting Dimension Detail (a child table of Accounting Dimension)."""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = ["AccountingDimensionDetailCreate", "AccountingDimensionDetailUpdate", "AccountingDimensionDetailRead", "AccountingDimensionDetailListResponse"]





class AccountingDimensionDetailCreate(InputSchema):

    company: Optional[Optional[str]] = None

    reference_document: Optional[Optional[str]] = None

    default_dimension: Optional[Optional[str]] = None

    mandatory_for_bs: bool

    mandatory_for_pl: bool

    automatically_post_balancing_accounting_entry: bool

    offsetting_account_id: Optional[Optional[uuid.UUID]] = None









class AccountingDimensionDetailUpdate(InputSchema):

    company: Optional[Optional[str]] = None

    reference_document: Optional[Optional[str]] = None

    default_dimension: Optional[Optional[str]] = None

    mandatory_for_bs: Optional[bool] = None

    mandatory_for_pl: Optional[bool] = None

    automatically_post_balancing_accounting_entry: Optional[bool] = None

    offsetting_account_id: Optional[Optional[uuid.UUID]] = None









class AccountingDimensionDetailRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    parent_id: Optional[uuid.UUID] = None

    idx: int

    company: Optional[Optional[str]] = None

    reference_document: Optional[Optional[str]] = None

    default_dimension: Optional[Optional[str]] = None

    mandatory_for_bs: bool

    mandatory_for_pl: bool

    automatically_post_balancing_accounting_entry: bool

    offsetting_account_id: Optional[Optional[uuid.UUID]] = None

    created_at: datetime

    updated_at: datetime





AccountingDimensionDetailListResponse = Page[AccountingDimensionDetailRead]

"""Pydantic v2 schemas for TaxWithholdingEntry."""





from __future__ import annotations

from app.accounts.tax_withholding_entry_domain.models.tax_withholding_entry import (

    TaxWithholdingEntryStatus,

    TaxWithholdingEntryUnderWithheldReason,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "TaxWithholdingEntryCreate",

    "TaxWithholdingEntryRead",

    "TaxWithholdingEntryListResponse",

]





class TaxWithholdingEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    tax_rate: Optional[Decimal] = None

    taxable_amount: Optional[Decimal] = None

    lower_deduction_certificate: Optional[str] = None

    status: Optional[TaxWithholdingEntryStatus] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    withholding_doctype: Optional[str] = None

    withholding_name: Optional[str] = None

    taxable_doctype: Optional[str] = None

    taxable_name: Optional[str] = None

    taxable_date: Optional[dt.date] = None

    withholding_date: Optional[dt.date] = None

    under_withheld_reason: Optional[TaxWithholdingEntryUnderWithheldReason] = None

    withholding_amount: Optional[Decimal] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    created_by_migration: Optional[bool] = None





class TaxWithholdingEntryCreate(TaxWithholdingEntryBase):

    """Accepted only nested inside the parent payload."""

    pass





class TaxWithholdingEntryRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    tax_rate: Optional[Decimal] = None

    taxable_amount: Optional[Decimal] = None

    lower_deduction_certificate: Optional[str] = None

    status: Optional[TaxWithholdingEntryStatus] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    withholding_doctype: Optional[str] = None

    withholding_name: Optional[str] = None

    taxable_doctype: Optional[str] = None

    taxable_name: Optional[str] = None

    taxable_date: Optional[dt.date] = None

    withholding_date: Optional[dt.date] = None

    under_withheld_reason: Optional[TaxWithholdingEntryUnderWithheldReason] = None

    withholding_amount: Optional[Decimal] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    created_by_migration: bool





TaxWithholdingEntryListResponse = Page[TaxWithholdingEntryRead]

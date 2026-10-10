"""Pydantic v2 schemas for TaxWithholdingRate (child table, read-only API)."""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal

from typing import Optional



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["TaxWithholdingRateCreate", "TaxWithholdingRateRead", "TaxWithholdingRateListResponse"]





class TaxWithholdingRateCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    tax_withholding_rate: Decimal

    single_threshold: Optional[Decimal] = None

    cumulative_threshold: Optional[Decimal] = None

    from_date: dt.date

    to_date: dt.date

    tax_withholding_group: Optional[str] = None





class TaxWithholdingRateRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    tax_withholding_rate: Optional[Decimal] = None

    single_threshold: Optional[Decimal] = None

    cumulative_threshold: Optional[Decimal] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    tax_withholding_group: Optional[str] = None





TaxWithholdingRateListResponse = Page[TaxWithholdingRateRead]

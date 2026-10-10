"""Pydantic v2 schemas for SupplierScorecardPeriod."""





from __future__ import annotations

from app.buying.supplier_scorecard_period_domain.models.supplier_scorecard_period import (

    SupplierScorecardPeriodNamingSeries,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.buying.supplier_scorecard_scoring_variable_domain.schemas.supplier_scorecard_scoring_variable import (

    SupplierScorecardScoringVariableCreate,

    SupplierScorecardScoringVariableRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierScorecardPeriodCreate",

    "SupplierScorecardPeriodUpdate",

    "SupplierScorecardPeriodRead",

    "SupplierScorecardPeriodListResponse",

]





class SupplierScorecardPeriodBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    supplier_id: uuid.UUID

    naming_series: SupplierScorecardPeriodNamingSeries

    total_score: Optional[Decimal] = None

    start_date: dt.date

    end_date: dt.date

    scorecard_id: uuid.UUID

    amended_from_id: Optional[uuid.UUID] = None

    variables: list[SupplierScorecardScoringVariableCreate] = []





class SupplierScorecardPeriodCreate(SupplierScorecardPeriodBase):

    pass





class SupplierScorecardPeriodUpdate(InputSchema):

    """A partial update."""



    supplier_id: Optional[uuid.UUID] = None

    naming_series: Optional[SupplierScorecardPeriodNamingSeries] = None

    total_score: Optional[Decimal] = None

    start_date: Optional[dt.date] = None

    end_date: Optional[dt.date] = None

    scorecard_id: Optional[uuid.UUID] = None

    amended_from_id: Optional[uuid.UUID] = None

    variables: Optional[list[SupplierScorecardScoringVariableCreate]] = None





class SupplierScorecardPeriodRead(ReadSchema):

    id: uuid.UUID

    name: str

    supplier_id: Optional[uuid.UUID] = None

    naming_series: Optional[SupplierScorecardPeriodNamingSeries] = None

    total_score: Optional[Decimal] = None

    start_date: Optional[dt.date] = None

    end_date: Optional[dt.date] = None

    scorecard_id: Optional[uuid.UUID] = None

    amended_from_id: Optional[uuid.UUID] = None

    variables: list[SupplierScorecardScoringVariableRead] = []





SupplierScorecardPeriodListResponse = Page[SupplierScorecardPeriodRead]

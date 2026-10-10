"""Pydantic v2 schemas for SupplierScorecardScoringCriteria."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierScorecardScoringCriteriaCreate",

    "SupplierScorecardScoringCriteriaRead",

    "SupplierScorecardScoringCriteriaListResponse",

]





class SupplierScorecardScoringCriteriaBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    criteria_name_id: uuid.UUID

    score: Optional[Decimal] = None

    weight: Decimal

    max_score: Optional[Decimal] = None

    formula: Optional[str] = None





class SupplierScorecardScoringCriteriaCreate(SupplierScorecardScoringCriteriaBase):

    pass





class SupplierScorecardScoringCriteriaUpdate(InputSchema):

    """A partial update."""



    criteria_name_id: Optional[uuid.UUID] = None

    score: Optional[Decimal] = None

    weight: Optional[Decimal] = None

    max_score: Optional[Decimal] = None

    formula: Optional[str] = None





class SupplierScorecardScoringCriteriaRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    criteria_name_id: Optional[uuid.UUID] = None

    score: Optional[Decimal] = None

    weight: Optional[Decimal] = None

    max_score: Optional[Decimal] = None

    formula: Optional[str] = None





SupplierScorecardScoringCriteriaListResponse = Page[SupplierScorecardScoringCriteriaRead]

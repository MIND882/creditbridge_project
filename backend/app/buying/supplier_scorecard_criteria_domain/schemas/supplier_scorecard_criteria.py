"""Pydantic v2 schemas for SupplierScorecardCriteria."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierScorecardCriteriaCreate",

    "SupplierScorecardCriteriaUpdate",

    "SupplierScorecardCriteriaRead",

    "SupplierScorecardCriteriaListResponse",

]





class SupplierScorecardCriteriaBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    criteria_name: str

    max_score: Decimal

    formula: str

    weight: Optional[Decimal] = None





class SupplierScorecardCriteriaCreate(SupplierScorecardCriteriaBase):

    pass





class SupplierScorecardCriteriaUpdate(InputSchema):

    """A partial update."""



    criteria_name: Optional[str] = None

    max_score: Optional[Decimal] = None

    formula: Optional[str] = None

    weight: Optional[Decimal] = None





class SupplierScorecardCriteriaRead(ReadSchema):

    id: uuid.UUID

    name: str

    criteria_name: str

    max_score: Optional[Decimal] = None

    formula: str

    weight: Optional[Decimal] = None





SupplierScorecardCriteriaListResponse = Page[SupplierScorecardCriteriaRead]

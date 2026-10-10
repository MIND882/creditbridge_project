"""Pydantic v2 schemas for SupplierScorecardScoringVariable."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierScorecardScoringVariableCreate",

    "SupplierScorecardScoringVariableRead",

    "SupplierScorecardScoringVariableListResponse",

]





class SupplierScorecardScoringVariableBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    variable_label_id: uuid.UUID

    description: Optional[str] = None

    value: Optional[Decimal] = None

    param_name: Optional[str] = None

    path: Optional[str] = None





class SupplierScorecardScoringVariableCreate(SupplierScorecardScoringVariableBase):

    pass





class SupplierScorecardScoringVariableUpdate(InputSchema):

    """A partial update."""



    variable_label_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    value: Optional[Decimal] = None

    param_name: Optional[str] = None

    path: Optional[str] = None





class SupplierScorecardScoringVariableRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    variable_label_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    value: Optional[Decimal] = None

    param_name: Optional[str] = None

    path: Optional[str] = None





SupplierScorecardScoringVariableListResponse = Page[SupplierScorecardScoringVariableRead]

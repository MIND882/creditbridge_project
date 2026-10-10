"""Pydantic v2 schemas for ItemQualityInspectionParameter."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemQualityInspectionParameterCreate",

    "ItemQualityInspectionParameterRead",

    "ItemQualityInspectionParameterListResponse",

]





class ItemQualityInspectionParameterBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    specification_id: uuid.UUID

    value: Optional[str] = None

    acceptance_formula: Optional[str] = None

    formula_based_criteria: Optional[bool] = None

    min_value: Optional[Decimal] = None

    max_value: Optional[Decimal] = None

    numeric: Optional[bool] = None

    parameter_group_id: Optional[uuid.UUID] = None





class ItemQualityInspectionParameterCreate(ItemQualityInspectionParameterBase):

    pass





class ItemQualityInspectionParameterUpdate(InputSchema):

    """A partial update."""



    specification_id: Optional[uuid.UUID] = None

    value: Optional[str] = None

    acceptance_formula: Optional[str] = None

    formula_based_criteria: Optional[bool] = None

    min_value: Optional[Decimal] = None

    max_value: Optional[Decimal] = None

    numeric: Optional[bool] = None

    parameter_group_id: Optional[uuid.UUID] = None





class ItemQualityInspectionParameterRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    specification_id: Optional[uuid.UUID] = None

    value: Optional[str] = None

    acceptance_formula: Optional[str] = None

    formula_based_criteria: Optional[bool] = None

    min_value: Optional[Decimal] = None

    max_value: Optional[Decimal] = None

    numeric: Optional[bool] = None

    parameter_group_id: Optional[uuid.UUID] = None





ItemQualityInspectionParameterListResponse = Page[ItemQualityInspectionParameterRead]

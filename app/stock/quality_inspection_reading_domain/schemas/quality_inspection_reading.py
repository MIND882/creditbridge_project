"""Pydantic v2 schemas for QualityInspectionReading."""





from __future__ import annotations

from app.stock.quality_inspection_reading_domain.models.quality_inspection_reading import (

    QualityInspectionReadingStatus,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "QualityInspectionReadingCreate",

    "QualityInspectionReadingRead",

    "QualityInspectionReadingListResponse",

]





class QualityInspectionReadingBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    specification_id: uuid.UUID

    value: Optional[str] = None

    reading_1: Optional[str] = None

    reading_2: Optional[str] = None

    reading_3: Optional[str] = None

    reading_4: Optional[str] = None

    reading_5: Optional[str] = None

    reading_6: Optional[str] = None

    reading_7: Optional[str] = None

    reading_8: Optional[str] = None

    reading_9: Optional[str] = None

    reading_10: Optional[str] = None

    status: Optional[QualityInspectionReadingStatus] = None

    acceptance_formula: Optional[str] = None

    formula_based_criteria: Optional[bool] = None

    min_value: Optional[Decimal] = None

    max_value: Optional[Decimal] = None

    reading_value: Optional[str] = None

    manual_inspection: Optional[bool] = None

    numeric: Optional[bool] = None

    parameter_group_id: Optional[uuid.UUID] = None





class QualityInspectionReadingCreate(QualityInspectionReadingBase):

    pass





class QualityInspectionReadingUpdate(InputSchema):

    """A partial update."""



    specification_id: Optional[uuid.UUID] = None

    value: Optional[str] = None

    reading_1: Optional[str] = None

    reading_2: Optional[str] = None

    reading_3: Optional[str] = None

    reading_4: Optional[str] = None

    reading_5: Optional[str] = None

    reading_6: Optional[str] = None

    reading_7: Optional[str] = None

    reading_8: Optional[str] = None

    reading_9: Optional[str] = None

    reading_10: Optional[str] = None

    status: Optional[QualityInspectionReadingStatus] = None

    acceptance_formula: Optional[str] = None

    formula_based_criteria: Optional[bool] = None

    min_value: Optional[Decimal] = None

    max_value: Optional[Decimal] = None

    reading_value: Optional[str] = None

    manual_inspection: Optional[bool] = None

    numeric: Optional[bool] = None

    parameter_group_id: Optional[uuid.UUID] = None





class QualityInspectionReadingRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    specification_id: Optional[uuid.UUID] = None

    value: Optional[str] = None

    reading_1: Optional[str] = None

    reading_2: Optional[str] = None

    reading_3: Optional[str] = None

    reading_4: Optional[str] = None

    reading_5: Optional[str] = None

    reading_6: Optional[str] = None

    reading_7: Optional[str] = None

    reading_8: Optional[str] = None

    reading_9: Optional[str] = None

    reading_10: Optional[str] = None

    status: Optional[QualityInspectionReadingStatus] = None

    acceptance_formula: Optional[str] = None

    formula_based_criteria: Optional[bool] = None

    min_value: Optional[Decimal] = None

    max_value: Optional[Decimal] = None

    reading_value: Optional[str] = None

    manual_inspection: Optional[bool] = None

    numeric: Optional[bool] = None

    parameter_group_id: Optional[uuid.UUID] = None





QualityInspectionReadingListResponse = Page[QualityInspectionReadingRead]

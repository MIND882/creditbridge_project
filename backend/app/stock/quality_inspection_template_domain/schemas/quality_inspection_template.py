"""Pydantic v2 schemas for QualityInspectionTemplate."""





from __future__ import annotations

from typing import Optional

import uuid



from app.stock.item_quality_inspection_parameter_domain.schemas.item_quality_inspection_parameter import (

    ItemQualityInspectionParameterCreate,

    ItemQualityInspectionParameterRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "QualityInspectionTemplateCreate",

    "QualityInspectionTemplateUpdate",

    "QualityInspectionTemplateRead",

    "QualityInspectionTemplateListResponse",

]





class QualityInspectionTemplateBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    quality_inspection_template_name: str

    item_quality_inspection_parameter: list[ItemQualityInspectionParameterCreate] = []





class QualityInspectionTemplateCreate(QualityInspectionTemplateBase):

    pass





class QualityInspectionTemplateUpdate(InputSchema):

    """A partial update."""



    quality_inspection_template_name: Optional[str] = None

    item_quality_inspection_parameter: Optional[list[ItemQualityInspectionParameterCreate]] = None





class QualityInspectionTemplateRead(ReadSchema):

    id: uuid.UUID

    name: str

    quality_inspection_template_name: str

    item_quality_inspection_parameter: list[ItemQualityInspectionParameterRead] = []





QualityInspectionTemplateListResponse = Page[QualityInspectionTemplateRead]

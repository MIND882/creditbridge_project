"""Pydantic v2 schemas for QualityInspectionParameter."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "QualityInspectionParameterCreate",

    "QualityInspectionParameterUpdate",

    "QualityInspectionParameterRead",

    "QualityInspectionParameterListResponse",

]





class QualityInspectionParameterBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parameter: str

    description: Optional[str] = None

    parameter_group_id: Optional[uuid.UUID] = None





class QualityInspectionParameterCreate(QualityInspectionParameterBase):

    pass





class QualityInspectionParameterUpdate(InputSchema):

    """A partial update."""



    parameter: Optional[str] = None

    description: Optional[str] = None

    parameter_group_id: Optional[uuid.UUID] = None





class QualityInspectionParameterRead(ReadSchema):

    id: uuid.UUID

    name: str

    parameter: str

    description: Optional[str] = None

    parameter_group_id: Optional[uuid.UUID] = None





QualityInspectionParameterListResponse = Page[QualityInspectionParameterRead]

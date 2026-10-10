"""Pydantic v2 schemas for QualityInspectionParameterGroup."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "QualityInspectionParameterGroupCreate",

    "QualityInspectionParameterGroupUpdate",

    "QualityInspectionParameterGroupRead",

    "QualityInspectionParameterGroupListResponse",

]





class QualityInspectionParameterGroupBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    group_name: str





class QualityInspectionParameterGroupCreate(QualityInspectionParameterGroupBase):

    pass





class QualityInspectionParameterGroupUpdate(InputSchema):

    """A partial update."""



    group_name: Optional[str] = None





class QualityInspectionParameterGroupRead(ReadSchema):

    id: uuid.UUID

    name: str

    group_name: str





QualityInspectionParameterGroupListResponse = Page[QualityInspectionParameterGroupRead]

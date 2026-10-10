"""Pydantic v2 schemas for SupplierScorecardVariable."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierScorecardVariableCreate",

    "SupplierScorecardVariableUpdate",

    "SupplierScorecardVariableRead",

    "SupplierScorecardVariableListResponse",

]





class SupplierScorecardVariableBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    variable_label: str

    is_custom: Optional[bool] = None

    param_name: str

    path: str

    description: Optional[str] = None





class SupplierScorecardVariableCreate(SupplierScorecardVariableBase):

    pass





class SupplierScorecardVariableUpdate(InputSchema):

    """A partial update."""



    variable_label: Optional[str] = None

    is_custom: Optional[bool] = None

    param_name: Optional[str] = None

    path: Optional[str] = None

    description: Optional[str] = None





class SupplierScorecardVariableRead(ReadSchema):

    id: uuid.UUID

    name: str

    variable_label: str

    is_custom: Optional[bool] = None

    param_name: str

    path: str

    description: Optional[str] = None





SupplierScorecardVariableListResponse = Page[SupplierScorecardVariableRead]

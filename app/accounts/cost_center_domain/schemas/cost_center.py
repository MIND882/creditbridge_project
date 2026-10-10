"""

Pydantic v2 schemas for Cost Center.



``is_group`` is absent from Update for the same reason it is on Account: the

group/ledger transition is guarded (child nodes, GL entries, allocation

records) and exposed as explicit conversion endpoints, not as an edit.

"""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "CostCenterBase",

    "CostCenterCreate",

    "CostCenterUpdate",

    "CostCenterRead",

    "CostCenterListResponse",

    "CostCenterTreeNode",

    "CostCenterTreeResponse",

    "CostCenterConvertResult",

]





class CostCenterBase(InputSchema):

    cost_center_name: Annotated[str, Field(min_length=1, max_length=140)]

    cost_center_number: Optional[Annotated[str, Field(max_length=140)]] = None

    disabled: bool = False



    @field_validator("cost_center_number", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class CostCenterCreate(CostCenterBase):

    parent_cost_center_id: Optional[uuid.UUID] = Field(

        default=None, description="Omit or null to create the root cost center"

    )

    is_group: bool = False





class CostCenterUpdate(InputSchema):

    cost_center_name: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None

    cost_center_number: Optional[Annotated[str, Field(max_length=140)]] = None

    parent_cost_center_id: Optional[uuid.UUID] = None

    disabled: Optional[bool] = None



    @field_validator("cost_center_number", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class CostCenterRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    cost_center_name: str

    cost_center_number: Optional[str] = None

    parent_cost_center_id: Optional[uuid.UUID] = None

    is_group: bool

    disabled: bool

    created_at: datetime

    updated_at: datetime





CostCenterListResponse = Page[CostCenterRead]





class CostCenterTreeNode(ReadSchema):

    id: uuid.UUID

    name: str

    cost_center_name: str

    cost_center_number: Optional[str] = None

    parent_cost_center_id: Optional[uuid.UUID] = None

    is_group: bool

    disabled: bool

    depth: int = 0

    children: list["CostCenterTreeNode"] = Field(default_factory=list)





CostCenterTreeNode.model_rebuild()





class CostCenterTreeResponse(ReadSchema):

    roots: list[CostCenterTreeNode]

    total_nodes: int





class CostCenterConvertResult(ReadSchema):

    id: uuid.UUID

    is_group: bool

    converted: bool = True

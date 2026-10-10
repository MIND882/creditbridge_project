"""Pydantic v2 contracts for Tax Category."""



from __future__ import annotations



import uuid

from typing import Optional



from pydantic import BaseModel, ConfigDict, Field, field_validator



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import ResultPage



__all__ = [

    "TaxCategoryCreate",

    "TaxCategoryUpdate",

    "TaxCategoryRead",

    "TaxCategoryListResponse",

]





class TaxCategoryCreate(InputSchema):

    title: str = Field(min_length=1, max_length=140)

    disabled: Optional[bool] = False



    @field_validator("title", mode="before")

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class TaxCategoryUpdate(InputSchema):

    """

    A partial update. ``title`` is the document's ``name``

    (``autoname = field:title``), so it is not renamable here.

    """



    disabled: Optional[bool] = Field(default=None)





class TaxCategoryRead(ReadSchema):

    id: uuid.UUID

    name: str

    title: str

    disabled: bool



    model_config = ConfigDict(from_attributes=True)





class TaxCategoryListResponse(BaseModel):

    items: list[TaxCategoryRead]

    total: int

    offset: int

    limit: int



    @classmethod

    def from_result(

        cls, result: ResultPage[object], items: list[TaxCategoryRead]

    ) -> "TaxCategoryListResponse":

        return cls(items=items, total=result.total, offset=result.offset, limit=result.limit)

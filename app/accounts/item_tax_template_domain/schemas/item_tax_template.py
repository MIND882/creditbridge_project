"""Pydantic v2 contracts for Item Tax Template."""



from __future__ import annotations



import uuid

from typing import Optional



from pydantic import BaseModel, ConfigDict, Field, field_validator



from app.accounts.item_tax_template_detail_domain.schemas.item_tax_template_detail import (

    ItemTaxTemplateDetailCreate,

    ItemTaxTemplateDetailRead,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import ResultPage



__all__ = [

    "ItemTaxTemplateCreate",

    "ItemTaxTemplateUpdate",

    "ItemTaxTemplateRead",

    "ItemTaxTemplateListResponse",

]





class ItemTaxTemplateCreate(InputSchema):

    title: str = Field(min_length=1, max_length=140)

    disabled: Optional[bool] = False



    #: Required upstream (``reqd=1``).

    taxes: list[ItemTaxTemplateDetailCreate] = Field(min_length=1)



    @field_validator("title", mode="before")

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class ItemTaxTemplateUpdate(InputSchema):

    """

    A partial update. ``title`` is the document's ``name``, so it is not

    renamable here.



    ``taxes`` replaces the whole child table when supplied.

    """



    disabled: Optional[bool] = Field(default=None)

    taxes: Optional[list[ItemTaxTemplateDetailCreate]] = Field(default=None, min_length=1)





class ItemTaxTemplateRead(ReadSchema):

    id: uuid.UUID

    name: str

    title: str

    disabled: bool

    taxes: list[ItemTaxTemplateDetailRead] = []



    model_config = ConfigDict(from_attributes=True)





class ItemTaxTemplateListResponse(BaseModel):

    items: list[ItemTaxTemplateRead]

    total: int

    offset: int

    limit: int



    @classmethod

    def from_result(

        cls, result: ResultPage[object], items: list[ItemTaxTemplateRead]

    ) -> "ItemTaxTemplateListResponse":

        return cls(items=items, total=result.total, offset=result.offset, limit=result.limit)

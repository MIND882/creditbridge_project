"""Pydantic v2 contracts for Dunning Type."""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from pydantic import BaseModel, ConfigDict, Field, field_validator



from app.accounts.dunning_letter_text_domain.schemas.dunning_letter_text import (

    DunningLetterTextCreate,

    DunningLetterTextRead,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import ResultPage



__all__ = [

    "DunningTypeCreate",

    "DunningTypeUpdate",

    "DunningTypeRead",

    "DunningTypeListResponse",

]





class DunningTypeCreate(InputSchema):

    dunning_type: str = Field(min_length=1, max_length=140)

    dunning_fee: Optional[Decimal] = Field(default=None)

    rate_of_interest: Optional[Decimal] = Field(default=None)

    is_default: Optional[bool] = False

    income_account_id: Optional[uuid.UUID] = Field(default=None)

    cost_center_id: Optional[uuid.UUID] = Field(default=None)

    dunning_letter_text: list[DunningLetterTextCreate] = Field(default_factory=list)



    @field_validator("dunning_type", mode="before")

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class DunningTypeUpdate(InputSchema):

    """

    A partial update. ``dunning_type`` is the document's ``name``, so it is not

    renamable here.



    ``dunning_letter_text`` replaces the whole child table when supplied.

    """



    dunning_fee: Optional[Decimal] = Field(default=None)

    rate_of_interest: Optional[Decimal] = Field(default=None)

    is_default: Optional[bool] = Field(default=None)

    income_account_id: Optional[uuid.UUID] = Field(default=None)

    cost_center_id: Optional[uuid.UUID] = Field(default=None)

    dunning_letter_text: Optional[list[DunningLetterTextCreate]] = Field(default=None)





class DunningTypeRead(ReadSchema):

    id: uuid.UUID

    name: str

    dunning_type: str

    dunning_fee: Optional[Decimal] = None

    rate_of_interest: Optional[Decimal] = None

    is_default: bool

    income_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    dunning_letter_text: list[DunningLetterTextRead] = []



    model_config = ConfigDict(from_attributes=True)





class DunningTypeListResponse(BaseModel):

    items: list[DunningTypeRead]

    total: int

    offset: int

    limit: int



    @classmethod

    def from_result(

        cls, result: ResultPage[object], items: list[DunningTypeRead]

    ) -> "DunningTypeListResponse":

        return cls(items=items, total=result.total, offset=result.offset, limit=result.limit)

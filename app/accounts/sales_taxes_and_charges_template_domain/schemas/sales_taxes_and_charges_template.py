"""Pydantic v2 contracts for Sales Taxes and Charges Template."""



from __future__ import annotations



import uuid

from typing import Optional



from pydantic import BaseModel, ConfigDict, Field, field_validator



from app.accounts.sales_taxes_and_charges_domain.schemas.sales_taxes_and_charges import (

    SalesTaxesAndChargesCreate,

    SalesTaxesAndChargesRead,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import ResultPage



__all__ = [

    "SalesTaxesAndChargesTemplateCreate",

    "SalesTaxesAndChargesTemplateUpdate",

    "SalesTaxesAndChargesTemplateRead",

    "SalesTaxesAndChargesTemplateListResponse",

]





class SalesTaxesAndChargesTemplateCreate(InputSchema):

    title: str = Field(min_length=1, max_length=140)

    is_default: Optional[bool] = False

    disabled: Optional[bool] = False

    tax_category_id: Optional[uuid.UUID] = Field(default=None)

    taxes: list[SalesTaxesAndChargesCreate] = Field(default_factory=list)



    @field_validator("title", mode="before")

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class SalesTaxesAndChargesTemplateUpdate(InputSchema):

    """

    A partial update. ``title`` is the document's ``name``, so it is not

    renamable here.



    ``taxes`` replaces the whole child table when supplied.

    """



    is_default: Optional[bool] = Field(default=None)

    disabled: Optional[bool] = Field(default=None)

    tax_category_id: Optional[uuid.UUID] = Field(default=None)

    taxes: Optional[list[SalesTaxesAndChargesCreate]] = Field(default=None)





class SalesTaxesAndChargesTemplateRead(ReadSchema):

    id: uuid.UUID

    name: str

    title: str

    is_default: bool

    disabled: bool

    tax_category_id: Optional[uuid.UUID] = None

    taxes: list[SalesTaxesAndChargesRead] = []



    model_config = ConfigDict(from_attributes=True)





class SalesTaxesAndChargesTemplateListResponse(BaseModel):

    items: list[SalesTaxesAndChargesTemplateRead]

    total: int

    offset: int

    limit: int



    @classmethod

    def from_result(

        cls, result: ResultPage[object], items: list[SalesTaxesAndChargesTemplateRead]

    ) -> "SalesTaxesAndChargesTemplateListResponse":

        return cls(items=items, total=result.total, offset=result.offset, limit=result.limit)

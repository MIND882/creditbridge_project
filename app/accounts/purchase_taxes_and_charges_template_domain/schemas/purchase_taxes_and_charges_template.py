"""Pydantic v2 contracts for Purchase Taxes and Charges Template."""



from __future__ import annotations



import uuid

from typing import Optional



from pydantic import BaseModel, ConfigDict, Field, field_validator



from app.accounts.purchase_taxes_and_charges_domain.schemas.purchase_taxes_and_charges import (

    PurchaseTaxesAndChargesCreate,

    PurchaseTaxesAndChargesRead,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import ResultPage



__all__ = [

    "PurchaseTaxesAndChargesTemplateCreate",

    "PurchaseTaxesAndChargesTemplateUpdate",

    "PurchaseTaxesAndChargesTemplateRead",

    "PurchaseTaxesAndChargesTemplateListResponse",

]





class PurchaseTaxesAndChargesTemplateCreate(InputSchema):

    title: str = Field(min_length=1, max_length=140)

    is_default: Optional[bool] = False

    disabled: Optional[bool] = False

    tax_category_id: Optional[uuid.UUID] = Field(default=None)

    taxes: list[PurchaseTaxesAndChargesCreate] = Field(default_factory=list)



    @field_validator("title", mode="before")

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class PurchaseTaxesAndChargesTemplateUpdate(InputSchema):

    """

    A partial update. ``title`` is the document's ``name``, so it is not

    renamable here.



    ``taxes`` replaces the whole child table when supplied.

    """



    is_default: Optional[bool] = Field(default=None)

    disabled: Optional[bool] = Field(default=None)

    tax_category_id: Optional[uuid.UUID] = Field(default=None)

    taxes: Optional[list[PurchaseTaxesAndChargesCreate]] = Field(default=None)





class PurchaseTaxesAndChargesTemplateRead(ReadSchema):

    id: uuid.UUID

    name: str

    title: str

    is_default: bool

    disabled: bool

    tax_category_id: Optional[uuid.UUID] = None

    taxes: list[PurchaseTaxesAndChargesRead] = []



    model_config = ConfigDict(from_attributes=True)





class PurchaseTaxesAndChargesTemplateListResponse(BaseModel):

    items: list[PurchaseTaxesAndChargesTemplateRead]

    total: int

    offset: int

    limit: int



    @classmethod

    def from_result(

        cls, result: ResultPage[object], items: list[PurchaseTaxesAndChargesTemplateRead]

    ) -> "PurchaseTaxesAndChargesTemplateListResponse":

        return cls(items=items, total=result.total, offset=result.offset, limit=result.limit)

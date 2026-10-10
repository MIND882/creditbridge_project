"""Pydantic v2 contracts for Payment Terms Template."""



from __future__ import annotations



import uuid

from typing import Optional



from pydantic import BaseModel, ConfigDict, Field, field_validator



from app.accounts.payment_terms_template_detail_domain.schemas.payment_terms_template_detail import (

    PaymentTermsTemplateDetailCreate,

    PaymentTermsTemplateDetailRead,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import ResultPage



__all__ = [

    "PaymentTermsTemplateCreate",

    "PaymentTermsTemplateUpdate",

    "PaymentTermsTemplateRead",

    "PaymentTermsTemplateListResponse",

]





class PaymentTermsTemplateCreate(InputSchema):

    template_name: str = Field(min_length=1, max_length=140)

    allocate_payment_based_on_payment_terms: Optional[bool] = False



    #: Required upstream (``reqd=1``); a template with no rows has no meaning.

    terms: list[PaymentTermsTemplateDetailCreate] = Field(min_length=1)



    @field_validator("template_name", mode="before")

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class PaymentTermsTemplateUpdate(InputSchema):

    """

    A partial update. ``template_name`` is the document's ``name``

    (``autoname = field:template_name``), so it is not renamable here.



    ``terms`` replaces the whole child table when supplied, which is how Frappe

    edits a child grid -- there is no partial-row patch.

    """



    allocate_payment_based_on_payment_terms: Optional[bool] = Field(default=None)

    terms: Optional[list[PaymentTermsTemplateDetailCreate]] = Field(default=None, min_length=1)





class PaymentTermsTemplateRead(ReadSchema):

    id: uuid.UUID

    name: str

    template_name: str

    allocate_payment_based_on_payment_terms: bool

    terms: list[PaymentTermsTemplateDetailRead] = []



    model_config = ConfigDict(from_attributes=True)





class PaymentTermsTemplateListResponse(BaseModel):

    items: list[PaymentTermsTemplateRead]

    total: int

    offset: int

    limit: int



    @classmethod

    def from_result(

        cls, result: ResultPage[object], items: list[PaymentTermsTemplateRead]

    ) -> "PaymentTermsTemplateListResponse":

        return cls(items=items, total=result.total, offset=result.offset, limit=result.limit)

"""Pydantic v2 contracts for Payment Term."""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from pydantic import BaseModel, ConfigDict, Field, field_validator



from app.accounts.payment_term_domain.models.payment_term import DiscountType, DueDateBasedOn

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import ResultPage



__all__ = [

    "PaymentTermCreate",

    "PaymentTermUpdate",

    "PaymentTermRead",

    "PaymentTermListResponse",

]





class PaymentTermBase(BaseModel):

    """Client-supplied fields. Never accepts ``business_id``."""



    payment_term_name: str = Field(min_length=1, max_length=140)

    invoice_portion: Optional[Decimal] = Field(default=None)

    mode_of_payment: Optional[str] = Field(default=None, max_length=140)

    due_date_based_on: Optional[DueDateBasedOn] = Field(default=None)

    credit_days: Optional[int] = Field(default=None)

    credit_months: Optional[int] = Field(default=None)

    description: Optional[str] = Field(default=None)

    discount_type: Optional[DiscountType] = Field(default=DiscountType.PERCENTAGE)

    discount: Optional[Decimal] = Field(default=None)

    discount_validity_based_on: Optional[DueDateBasedOn] = Field(

        default=DueDateBasedOn.DAYS_AFTER_INVOICE_DATE

    )

    discount_validity: Optional[int] = Field(default=None)





class PaymentTermCreate(PaymentTermBase, InputSchema):

    @field_validator(

        "mode_of_payment", "description", mode="before"

    )

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class PaymentTermUpdate(InputSchema):

    """

    A partial update. ``payment_term_name`` is the document's ``name``

    (``autoname = field:payment_term_name``), so renaming it is an identity

    change and is refused here rather than silently re-keying every template

    row that points at it.

    """



    invoice_portion: Optional[Decimal] = Field(default=None)

    mode_of_payment: Optional[str] = Field(default=None, max_length=140)

    due_date_based_on: Optional[DueDateBasedOn] = Field(default=None)

    credit_days: Optional[int] = Field(default=None)

    credit_months: Optional[int] = Field(default=None)

    description: Optional[str] = Field(default=None)

    discount_type: Optional[DiscountType] = Field(default=None)

    discount: Optional[Decimal] = Field(default=None)

    discount_validity_based_on: Optional[DueDateBasedOn] = Field(default=None)

    discount_validity: Optional[int] = Field(default=None)



    @field_validator("mode_of_payment", "description", mode="before")

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class PaymentTermRead(PaymentTermBase, ReadSchema):

    id: uuid.UUID

    name: str



    model_config = ConfigDict(from_attributes=True)





class PaymentTermListResponse(BaseModel):

    items: list[PaymentTermRead]

    total: int

    offset: int

    limit: int



    @classmethod

    def from_result(

        cls, result: ResultPage[object], items: list[PaymentTermRead]

    ) -> "PaymentTermListResponse":

        return cls(items=items, total=result.total, offset=result.offset, limit=result.limit)

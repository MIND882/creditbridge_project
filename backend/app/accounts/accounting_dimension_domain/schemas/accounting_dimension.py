"""Pydantic v2 schemas for Accounting Dimension."""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "AccountingDimensionDetailCreate",

    "AccountingDimensionDetailRead",

    "AccountingDimensionCreate",

    "AccountingDimensionUpdate",

    "AccountingDimensionRead",

    "AccountingDimensionListResponse",

]





class AccountingDimensionDetailCreate(InputSchema):

    """

    One per-company default for the dimension.



    ``default_dimension`` is ERPNext's Dynamic Link resolved against

    ``reference_document`` -- a label plus the doctype that gives it meaning.

    """



    company: Optional[Annotated[str, Field(max_length=140)]] = None

    reference_document: Optional[Annotated[str, Field(max_length=140)]] = None

    default_dimension: Optional[Annotated[str, Field(max_length=140)]] = None

    mandatory_for_bs: bool = False

    mandatory_for_pl: bool = False

    automatically_post_balancing_accounting_entry: bool = False

    offsetting_account_id: Optional[uuid.UUID] = None



    @field_validator("company", "reference_document", "default_dimension", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountingDimensionDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    company: Optional[str] = None

    reference_document: Optional[str] = None

    default_dimension: Optional[str] = None

    mandatory_for_bs: bool

    mandatory_for_pl: bool

    automatically_post_balancing_accounting_entry: bool

    offsetting_account_id: Optional[uuid.UUID] = None





class AccountingDimensionCreate(InputSchema):

    label: Annotated[str, Field(min_length=1, max_length=140)]

    document_type: Annotated[str, Field(min_length=1, max_length=140)]

    fieldname: Optional[Annotated[str, Field(max_length=140)]] = Field(

        default=None,

        description="Derived from `label` when omitted",

    )

    disabled: bool = False

    dimension_defaults: list[AccountingDimensionDetailCreate] = Field(default_factory=list)



    @field_validator("fieldname", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountingDimensionUpdate(InputSchema):

    """

    ``document_type`` is absent: it decides what the dimension's values *are*,

    so changing it would orphan every stored value and default. Cancel and

    recreate instead.

    """



    label: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None

    fieldname: Optional[Annotated[str, Field(max_length=140)]] = None

    disabled: Optional[bool] = None

    dimension_defaults: Optional[list[AccountingDimensionDetailCreate]] = None



    @field_validator("fieldname", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountingDimensionRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    label: str

    fieldname: str

    document_type: str

    disabled: bool

    dimension_defaults: list[AccountingDimensionDetailRead] = Field(default_factory=list)

    created_at: datetime

    updated_at: datetime





AccountingDimensionListResponse = Page[AccountingDimensionRead]

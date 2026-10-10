"""Pydantic v2 schemas for Accounting Dimension Filter."""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.accounts.accounting_dimension_filter_domain.models.accounting_dimension_filter import (

    AllowOrRestrict,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "ApplicableOnAccountCreate",

    "AllowedDimensionCreate",

    "AccountingDimensionFilterCreate",

    "AccountingDimensionFilterUpdate",

    "AccountingDimensionFilterRead",

    "AccountingDimensionFilterListResponse",

]





class ApplicableOnAccountCreate(InputSchema):

    """Which accounts this filter governs, and whether the rule is mandatory."""



    account_id: uuid.UUID

    is_mandatory: bool = False





class AllowedDimensionCreate(InputSchema):

    """A permitted (or forbidden) value for the dimension."""



    accounting_dimension: Optional[Annotated[str, Field(max_length=140)]] = None

    dimension_value: Optional[Annotated[str, Field(max_length=140)]] = None



    @field_validator("accounting_dimension", "dimension_value", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountingDimensionFilterCreate(InputSchema):

    accounting_dimension: Annotated[str, Field(min_length=1, max_length=140)]

    allow_or_restrict: AllowOrRestrict

    accounts: Annotated[list[ApplicableOnAccountCreate], Field(min_length=1)] = Field(

        description="At least one account is required (reqd=1 upstream)"

    )

    dimensions: list[AllowedDimensionCreate] = Field(default_factory=list)

    fieldname: Optional[Annotated[str, Field(max_length=140)]] = None

    apply_restriction_on_values: bool = False

    disabled: bool = False



    @field_validator("fieldname", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountingDimensionFilterUpdate(InputSchema):

    """

    ``accounting_dimension`` is absent: it is what the whole filter (and its

    generated name) is keyed on, so changing it would silently retarget the

    rule. Delete and recreate instead.

    """



    allow_or_restrict: Optional[AllowOrRestrict] = None

    accounts: Optional[Annotated[list[ApplicableOnAccountCreate], Field(min_length=1)]] = None

    dimensions: Optional[list[AllowedDimensionCreate]] = None

    fieldname: Optional[Annotated[str, Field(max_length=140)]] = None

    apply_restriction_on_values: Optional[bool] = None

    disabled: Optional[bool] = None



    @field_validator("fieldname", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class ApplicableOnAccountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    account_id: uuid.UUID

    is_mandatory: bool





class AllowedDimensionRead(ReadSchema):

    id: uuid.UUID

    idx: int

    accounting_dimension: Optional[str] = None

    dimension_value: Optional[str] = None





class AccountingDimensionFilterRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    accounting_dimension: str

    fieldname: Optional[str] = None

    allow_or_restrict: AllowOrRestrict

    apply_restriction_on_values: bool

    disabled: bool

    accounts: list[ApplicableOnAccountRead] = Field(default_factory=list)

    dimensions: list[AllowedDimensionRead] = Field(default_factory=list)

    created_at: datetime

    updated_at: datetime





AccountingDimensionFilterListResponse = Page[AccountingDimensionFilterRead]

"""Pydantic v2 contracts for Tax Withholding Category."""



from __future__ import annotations



import uuid

from typing import Optional



from pydantic import BaseModel, ConfigDict, Field, field_validator



from app.accounts.tax_withholding_account_domain.schemas.tax_withholding_account import (

    TaxWithholdingAccountCreate,

    TaxWithholdingAccountRead,

)

from app.accounts.tax_withholding_category_domain.models.tax_withholding_category import (

    TaxDeductionBasis,

)

from app.accounts.tax_withholding_rate_domain.schemas.tax_withholding_rate import (

    TaxWithholdingRateCreate,

    TaxWithholdingRateRead,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import ResultPage



__all__ = [

    "TaxWithholdingCategoryCreate",

    "TaxWithholdingCategoryUpdate",

    "TaxWithholdingCategoryRead",

    "TaxWithholdingCategoryListResponse",

]





class TaxWithholdingCategoryCreate(InputSchema):

    category_name: str = Field(min_length=1, max_length=140)



    #: Both required upstream (``reqd=1``).

    rates: list[TaxWithholdingRateCreate] = Field(min_length=1)

    accounts: list[TaxWithholdingAccountCreate] = Field(min_length=1)



    tax_on_excess_amount: Optional[bool] = False

    round_off_tax_amount: Optional[bool] = False

    tax_deduction_basis: Optional[TaxDeductionBasis] = TaxDeductionBasis.NET_TOTAL

    disable_cumulative_threshold: Optional[bool] = False

    disable_transaction_threshold: Optional[bool] = False



    @field_validator("category_name", mode="before")

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class TaxWithholdingCategoryUpdate(InputSchema):

    """

    A partial update. ``category_name`` is the document's ``name``

    (``autoname = Prompt``), so it is not renamable here.



    Each child table is replaced wholesale when supplied, matching how Frappe

    edits a grid.

    """



    rates: Optional[list[TaxWithholdingRateCreate]] = Field(default=None, min_length=1)

    accounts: Optional[list[TaxWithholdingAccountCreate]] = Field(default=None, min_length=1)

    tax_on_excess_amount: Optional[bool] = Field(default=None)

    round_off_tax_amount: Optional[bool] = Field(default=None)

    tax_deduction_basis: Optional[TaxDeductionBasis] = Field(default=None)

    disable_cumulative_threshold: Optional[bool] = Field(default=None)

    disable_transaction_threshold: Optional[bool] = Field(default=None)





class TaxWithholdingCategoryRead(ReadSchema):

    id: uuid.UUID

    name: str

    category_name: Optional[str] = None

    tax_on_excess_amount: bool

    round_off_tax_amount: bool

    tax_deduction_basis: Optional[TaxDeductionBasis] = None

    disable_cumulative_threshold: bool

    disable_transaction_threshold: bool

    rates: list[TaxWithholdingRateRead] = []

    accounts: list[TaxWithholdingAccountRead] = []



    model_config = ConfigDict(from_attributes=True)





class TaxWithholdingCategoryListResponse(BaseModel):

    items: list[TaxWithholdingCategoryRead]

    total: int

    offset: int

    limit: int



    @classmethod

    def from_result(

        cls, result: ResultPage[object], items: list[TaxWithholdingCategoryRead]

    ) -> "TaxWithholdingCategoryListResponse":

        return cls(items=items, total=result.total, offset=result.offset, limit=result.limit)

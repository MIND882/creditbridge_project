"""

Pydantic v2 schemas for Payment Entry.



The derived amounts (``unallocated_amount``, ``total_allocated_amount``,

``total_deduction_amount``, ``difference_amount``, ``status``) and ``docstatus``

appear only in ``Read``.

"""



from __future__ import annotations



import datetime as dt

import uuid

from datetime import datetime

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.accounts.payment_entry_deduction_domain.schemas.payment_entry_deduction import (

    PaymentEntryDeductionCreate,

    PaymentEntryDeductionRead,

)

from app.accounts.payment_entry_domain.models.payment_entry import NAMING_SERIES, PaymentType

from app.accounts.payment_entry_reference_domain.schemas.payment_entry_reference import (

    PaymentEntryReferenceCreate,

    PaymentEntryReferenceRead,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "PaymentEntryCreate",

    "PaymentEntryUpdate",

    "PaymentEntryRead",

    "PaymentEntryListResponse",

    "PaymentEntryStatusResult",

]



_STR = Annotated[str, Field(max_length=140)]





class PaymentEntryCreate(InputSchema):

    payment_type: PaymentType

    posting_date: dt.date

    paid_from_id: uuid.UUID

    paid_to_id: uuid.UUID

    paid_amount: Decimal = Field(gt=0)

    source_exchange_rate: float = Field(default=1.0, gt=0)

    target_exchange_rate: float = Field(default=1.0, gt=0)



    naming_series: _STR = Field(default=NAMING_SERIES)

    received_amount: Optional[Decimal] = Field(default=None, ge=0)

    paid_from_account_currency: Optional[_STR] = None

    paid_to_account_currency: Optional[_STR] = None

    party_type: Optional[_STR] = None

    party: Optional[_STR] = None

    party_name: Optional[_STR] = None

    cost_center_id: Optional[uuid.UUID] = None

    mode_of_payment: Optional[_STR] = None

    bank_account_id: Optional[uuid.UUID] = None

    party_bank_account_id: Optional[uuid.UUID] = None

    reference_no: Optional[_STR] = None

    reference_date: Optional[dt.date] = None

    project: Optional[_STR] = None

    remarks: Optional[str] = None

    title: Optional[_STR] = None

    is_opening: bool = False

    apply_tds: bool = False



    references: list[PaymentEntryReferenceCreate] = Field(default_factory=list)

    deductions: list[PaymentEntryDeductionCreate] = Field(default_factory=list)



    @field_validator(

        "paid_from_account_currency", "paid_to_account_currency", "party_type", "party",

        "party_name", "mode_of_payment", "reference_no", "project", "title",

        mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class PaymentEntryUpdate(InputSchema):

    """

    ``payment_type``, ``paid_from_id`` and ``paid_to_id`` are absent: together

    they decide the direction of the money and which accounts the GL entries

    hit, so changing them would silently invalidate what was posted.

    """



    posting_date: Optional[dt.date] = None

    paid_amount: Optional[Decimal] = Field(default=None, gt=0)

    received_amount: Optional[Decimal] = Field(default=None, ge=0)

    source_exchange_rate: Optional[float] = Field(default=None, gt=0)

    target_exchange_rate: Optional[float] = Field(default=None, gt=0)

    party_type: Optional[_STR] = None

    party: Optional[_STR] = None

    party_name: Optional[_STR] = None

    cost_center_id: Optional[uuid.UUID] = None

    mode_of_payment: Optional[_STR] = None

    bank_account_id: Optional[uuid.UUID] = None

    reference_no: Optional[_STR] = None

    reference_date: Optional[dt.date] = None

    project: Optional[_STR] = None

    remarks: Optional[str] = None

    title: Optional[_STR] = None

    references: Optional[list[PaymentEntryReferenceCreate]] = None

    deductions: Optional[list[PaymentEntryDeductionCreate]] = None



    @field_validator(

        "party_type", "party", "party_name", "mode_of_payment", "reference_no",

        "project", "title",

        mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class PaymentEntryRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    naming_series: str

    title: Optional[str] = None

    payment_type: PaymentType

    posting_date: dt.date

    paid_from_id: uuid.UUID

    paid_to_id: uuid.UUID

    paid_amount: Decimal

    received_amount: Optional[Decimal] = None

    source_exchange_rate: float

    target_exchange_rate: float

    paid_from_account_currency: Optional[str] = None

    paid_to_account_currency: Optional[str] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    party_name: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    mode_of_payment: Optional[str] = None

    bank_account_id: Optional[uuid.UUID] = None

    party_bank_account_id: Optional[uuid.UUID] = None

    reference_no: Optional[str] = None

    reference_date: Optional[dt.date] = None

    project: Optional[str] = None

    remarks: Optional[str] = None

    is_opening: str

    apply_tds: bool

    unallocated_amount: Optional[Decimal] = None

    total_allocated_amount: Optional[Decimal] = None

    total_deduction_amount: Optional[Decimal] = None

    difference_amount: Optional[Decimal] = None

    status: str

    references: list[PaymentEntryReferenceRead] = Field(default_factory=list)

    deductions: list[PaymentEntryDeductionRead] = Field(default_factory=list)

    docstatus: int

    amended_from_id: Optional[uuid.UUID] = None

    created_at: datetime

    updated_at: datetime





PaymentEntryListResponse = Page[PaymentEntryRead]





class PaymentEntryStatusResult(ReadSchema):

    id: uuid.UUID

    name: str

    docstatus: int

    status: str

    difference_amount: Optional[Decimal] = None

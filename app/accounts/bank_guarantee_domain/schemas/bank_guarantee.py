"""

Pydantic v2 schemas for Bank Guarantee.



``docstatus`` is absent from every input schema: the lifecycle moves through

``/submit``, ``/cancel`` and ``/amend``. The three fields ``on_submit`` requires

(``bank_guarantee_number``, ``name_of_beneficiary``, ``bank``) stay optional on

create for the same reason -- upstream only demands them at submit time.

"""



from __future__ import annotations



import uuid

from datetime import date, datetime

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.accounts.bank_guarantee_domain.models.bank_guarantee import BGType

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "BankGuaranteeCreate",

    "BankGuaranteeUpdate",

    "BankGuaranteeRead",

    "BankGuaranteeListResponse",

    "BankGuaranteeStatusResult",

]



_STR = Annotated[str, Field(max_length=140)]





class BankGuaranteeCreate(InputSchema):

    bg_type: BGType

    amount: Decimal = Field(gt=0)

    start_date: date

    validity: Optional[int] = Field(default=None, ge=0)

    end_date: Optional[date] = None



    customer: Optional[_STR] = None

    supplier: Optional[_STR] = None

    project: Optional[_STR] = None

    reference_doctype: Optional[_STR] = None

    reference_docname: Optional[_STR] = None



    bank_id: Optional[uuid.UUID] = None

    bank_account_id: Optional[uuid.UUID] = None

    account_id: Optional[uuid.UUID] = None



    bank_account_no: Optional[_STR] = None

    iban: Optional[_STR] = None

    branch_code: Optional[_STR] = None

    swift_number: Optional[_STR] = None



    bank_guarantee_number: Optional[_STR] = None

    name_of_beneficiary: Optional[_STR] = None

    fixed_deposit_number: Optional[_STR] = None



    margin_money: Optional[Decimal] = Field(default=None, ge=0)

    charges: Optional[Decimal] = Field(default=None, ge=0)

    more_information: Optional[str] = None



    @field_validator(

        "customer", "supplier", "project", "reference_doctype", "reference_docname",

        "bank_account_no", "iban", "branch_code", "swift_number",

        "bank_guarantee_number", "name_of_beneficiary", "fixed_deposit_number",

        mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankGuaranteeUpdate(InputSchema):

    """

    ``bg_type`` is absent: it decides whether the counterparty is a customer or

    a supplier, so flipping it would invalidate whichever was set. Cancel and

    recreate instead.

    """



    amount: Optional[Decimal] = Field(default=None, gt=0)

    start_date: Optional[date] = None

    validity: Optional[int] = Field(default=None, ge=0)

    end_date: Optional[date] = None



    customer: Optional[_STR] = None

    supplier: Optional[_STR] = None

    project: Optional[_STR] = None

    reference_doctype: Optional[_STR] = None

    reference_docname: Optional[_STR] = None



    bank_id: Optional[uuid.UUID] = None

    bank_account_id: Optional[uuid.UUID] = None

    account_id: Optional[uuid.UUID] = None



    bank_account_no: Optional[_STR] = None

    iban: Optional[_STR] = None

    branch_code: Optional[_STR] = None

    swift_number: Optional[_STR] = None



    bank_guarantee_number: Optional[_STR] = None

    name_of_beneficiary: Optional[_STR] = None

    fixed_deposit_number: Optional[_STR] = None



    margin_money: Optional[Decimal] = Field(default=None, ge=0)

    charges: Optional[Decimal] = Field(default=None, ge=0)

    more_information: Optional[str] = None



    @field_validator(

        "customer", "supplier", "project", "reference_doctype", "reference_docname",

        "bank_account_no", "iban", "branch_code", "swift_number",

        "bank_guarantee_number", "name_of_beneficiary", "fixed_deposit_number",

        mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankGuaranteeRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    bg_type: BGType

    amount: Decimal

    start_date: date

    validity: Optional[int] = None

    end_date: Optional[date] = None

    customer: Optional[str] = None

    supplier: Optional[str] = None

    project: Optional[str] = None

    reference_doctype: Optional[str] = None

    reference_docname: Optional[str] = None

    bank_id: Optional[uuid.UUID] = None

    bank_account_id: Optional[uuid.UUID] = None

    account_id: Optional[uuid.UUID] = None

    bank_account_no: Optional[str] = None

    iban: Optional[str] = None

    branch_code: Optional[str] = None

    swift_number: Optional[str] = None

    bank_guarantee_number: Optional[str] = None

    name_of_beneficiary: Optional[str] = None

    fixed_deposit_number: Optional[str] = None

    margin_money: Optional[Decimal] = None

    charges: Optional[Decimal] = None

    more_information: Optional[str] = None

    docstatus: int

    amended_from_id: Optional[uuid.UUID] = None

    created_at: datetime

    updated_at: datetime





BankGuaranteeListResponse = Page[BankGuaranteeRead]





class BankGuaranteeStatusResult(ReadSchema):

    id: uuid.UUID

    name: str

    docstatus: int

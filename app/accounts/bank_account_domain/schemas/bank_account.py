"""Pydantic v2 schemas for Bank Account."""



from __future__ import annotations



import uuid

from datetime import date, datetime

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "BankAccountBalanceCreate",

    "BankAccountBalanceRead",

    "BankAccountCreate",

    "BankAccountUpdate",

    "BankAccountRead",

    "BankAccountListResponse",

]



_STR = Annotated[str, Field(max_length=140)]





class BankAccountBalanceCreate(InputSchema):

    date: date

    balance: Decimal

    currency: Optional[_STR] = None



    @field_validator("currency", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankAccountBalanceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    date: date

    balance: Decimal

    currency: Optional[str] = None





class BankAccountCreate(InputSchema):

    account_name: Annotated[str, Field(min_length=1, max_length=140)]

    bank_id: uuid.UUID

    account_id: Optional[uuid.UUID] = None

    account_type: Optional[_STR] = None

    account_subtype: Optional[_STR] = None

    is_default: bool = False

    is_company_account: bool = False

    is_credit_card: bool = False

    disabled: bool = False

    party_type: Optional[_STR] = None

    party: Optional[_STR] = None

    iban: Optional[_STR] = None

    bank_account_no: Optional[_STR] = None

    mask: Optional[_STR] = None

    branch_code: Optional[_STR] = None

    balances: list[BankAccountBalanceCreate] = Field(default_factory=list)



    @field_validator(

        "account_type", "account_subtype", "party_type", "party",

        "iban", "bank_account_no", "mask", "branch_code", mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankAccountUpdate(InputSchema):

    """

    ``bank_id`` is absent: upstream's ``autoname`` derives the document name

    from ``account_name + " - " + bank``, so moving an account between banks

    would change its identity. Cancel and recreate instead.

    """



    account_name: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None

    account_id: Optional[uuid.UUID] = None

    account_type: Optional[_STR] = None

    account_subtype: Optional[_STR] = None

    is_default: Optional[bool] = None

    is_company_account: Optional[bool] = None

    is_credit_card: Optional[bool] = None

    disabled: Optional[bool] = None

    party_type: Optional[_STR] = None

    party: Optional[_STR] = None

    iban: Optional[_STR] = None

    bank_account_no: Optional[_STR] = None

    mask: Optional[_STR] = None

    branch_code: Optional[_STR] = None

    balances: Optional[list[BankAccountBalanceCreate]] = None



    @field_validator(

        "account_type", "account_subtype", "party_type", "party",

        "iban", "bank_account_no", "mask", "branch_code", mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankAccountRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    account_name: str

    bank_id: uuid.UUID

    account_id: Optional[uuid.UUID] = None

    account_type: Optional[str] = None

    account_subtype: Optional[str] = None

    is_default: bool

    is_company_account: bool

    is_credit_card: bool

    disabled: bool

    party_type: Optional[str] = None

    party: Optional[str] = None

    iban: Optional[str] = None

    bank_account_no: Optional[str] = None

    mask: Optional[str] = None

    branch_code: Optional[str] = None

    last_integration_date: Optional[date] = None

    balances: list[BankAccountBalanceRead] = Field(default_factory=list)

    created_at: datetime

    updated_at: datetime





BankAccountListResponse = Page[BankAccountRead]

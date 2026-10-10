"""

Pydantic v2 schemas for GL Entry.



GL Entries are append-only, so there is no ``Update`` schema: a correction is a

reversal posted as a new entry. ``docstatus`` and ``is_cancelled`` are both

excluded from input -- they move only through the cancel endpoint.

"""



from __future__ import annotations



import uuid

from datetime import datetime

from decimal import Decimal

import datetime as dt

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.accounts.gl_entry_domain.models.gl_entry import YesNo

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = ["GLEntryCreate", "GLEntryRead", "GLEntryListResponse", "GLEntryStatusResult"]



_STR = Annotated[str, Field(max_length=140)]





class GLEntryCreate(InputSchema):

    posting_date: dt.date

    account_id: uuid.UUID

    voucher_type: Annotated[str, Field(min_length=1, max_length=140)]

    voucher_no: Annotated[str, Field(min_length=1, max_length=140)]



    #: One side is expected to be zero; the service rejects a both-zero entry.

    debit: Optional[Decimal] = Field(default=None, ge=0)

    credit: Optional[Decimal] = Field(default=None, ge=0)



    transaction_date: Optional[dt.date] = None

    cost_center_id: Optional[uuid.UUID] = None

    finance_book_id: Optional[uuid.UUID] = None



    party_type: Optional[_STR] = None

    party: Optional[_STR] = None



    account_currency: Optional[_STR] = None

    debit_in_account_currency: Optional[Decimal] = None

    credit_in_account_currency: Optional[Decimal] = None



    transaction_currency: Optional[_STR] = None

    transaction_exchange_rate: Optional[float] = None

    debit_in_transaction_currency: Optional[Decimal] = None

    credit_in_transaction_currency: Optional[Decimal] = None



    against: Optional[str] = None

    voucher_detail_no: Optional[_STR] = None

    voucher_subtype: Optional[str] = None

    against_voucher_type: Optional[_STR] = None

    against_voucher: Optional[_STR] = None

    project: Optional[_STR] = None

    remarks: Optional[str] = None

    is_opening: YesNo = YesNo.NO

    is_advance: YesNo = YesNo.NO

    fiscal_year: Optional[_STR] = None

    due_date: Optional[dt.date] = None



    @field_validator(

        "party_type", "party", "account_currency", "transaction_currency",

        "voucher_detail_no", "against_voucher_type", "against_voucher", "project",

        "fiscal_year",

        mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class GLEntryRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    posting_date: dt.date

    transaction_date: Optional[dt.date] = None

    account_id: uuid.UUID

    cost_center_id: Optional[uuid.UUID] = None

    finance_book_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    debit: Decimal

    credit: Decimal

    account_currency: Optional[str] = None

    debit_in_account_currency: Optional[Decimal] = None

    credit_in_account_currency: Optional[Decimal] = None

    transaction_currency: Optional[str] = None

    transaction_exchange_rate: Optional[float] = None

    debit_in_transaction_currency: Optional[Decimal] = None

    credit_in_transaction_currency: Optional[Decimal] = None

    debit_in_reporting_currency: Optional[Decimal] = None

    credit_in_reporting_currency: Optional[Decimal] = None

    reporting_currency_exchange_rate: Optional[float] = None

    against: Optional[str] = None

    voucher_type: str

    voucher_no: str

    voucher_detail_no: Optional[str] = None

    voucher_subtype: Optional[str] = None

    against_voucher_type: Optional[str] = None

    against_voucher: Optional[str] = None

    project: Optional[str] = None

    remarks: Optional[str] = None

    is_opening: YesNo

    is_advance: YesNo

    fiscal_year: Optional[str] = None

    to_rename: bool

    due_date: Optional[dt.date] = None

    is_cancelled: bool

    docstatus: int

    created_at: datetime

    updated_at: datetime





GLEntryListResponse = Page[GLEntryRead]





class GLEntryStatusResult(ReadSchema):

    id: uuid.UUID

    name: str

    docstatus: int

    is_cancelled: bool





class AccountBalanceRead(ReadSchema):

    """

    The ``debit - credit`` sum for one account.



    Excludes cancelled entries, matching upstream's ``is_cancelled == 0`` filter

    on every balance query.

    """



    account_id: uuid.UUID

    balance: Decimal

    total_debit: Decimal

    total_credit: Decimal

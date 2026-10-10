"""

Pydantic v2 schemas for Journal Entry.



``total_debit``, ``total_credit``, ``difference`` and ``docstatus`` are derived,

so they appear only in ``Read``. ``is_opening`` is accepted on input but the

service forces it to ``Yes`` for an Opening Entry voucher, matching upstream.

"""



from __future__ import annotations



import datetime as dt

import uuid

from datetime import datetime

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.accounts.journal_entry_account_domain.schemas.journal_entry_account import (

    JournalEntryAccountCreate,

    JournalEntryAccountRead,

)

from app.accounts.journal_entry_domain.models.journal_entry import (

    NAMING_SERIES,

    JournalVoucherType,

    WriteOffBasedOn,

    YesNo,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "JournalEntryCreate",

    "JournalEntryUpdate",

    "JournalEntryRead",

    "JournalEntryListResponse",

    "JournalEntryStatusResult",

]



_STR = Annotated[str, Field(max_length=140)]





class JournalEntryCreate(InputSchema):

    posting_date: dt.date

    voucher_type: JournalVoucherType = JournalVoucherType.JOURNAL_ENTRY

    accounts: Annotated[list[JournalEntryAccountCreate], Field(min_length=1)]



    naming_series: _STR = Field(default=NAMING_SERIES)

    title: Optional[_STR] = None

    cheque_no: Optional[_STR] = None

    cheque_date: Optional[dt.date] = None

    user_remark: Optional[str] = None

    bill_no: Optional[_STR] = None

    bill_date: Optional[dt.date] = None

    due_date: Optional[dt.date] = None

    multi_currency: bool = False

    pay_to_recd_from: Optional[_STR] = None

    mode_of_payment: Optional[_STR] = None

    is_opening: YesNo = YesNo.NO

    write_off_based_on: WriteOffBasedOn = WriteOffBasedOn.ACCOUNTS_RECEIVABLE

    write_off_amount: Optional[Decimal] = Field(default=None, ge=0)

    party_not_required: bool = False

    custom_remark: bool = False

    apply_tds: bool = False



    @field_validator("title", "cheque_no", "bill_no", "pay_to_recd_from", "mode_of_payment", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class JournalEntryUpdate(InputSchema):

    """

    ``voucher_type`` and ``posting_date`` are absent: both drive derived state

    (the opening-entry rules and the GL Entry dates), so changing either would

    silently invalidate what was already posted. Cancel and re-post instead.

    """



    title: Optional[_STR] = None

    cheque_no: Optional[_STR] = None

    cheque_date: Optional[dt.date] = None

    user_remark: Optional[str] = None

    bill_no: Optional[_STR] = None

    bill_date: Optional[dt.date] = None

    due_date: Optional[dt.date] = None

    pay_to_recd_from: Optional[_STR] = None

    mode_of_payment: Optional[_STR] = None

    write_off_amount: Optional[Decimal] = Field(default=None, ge=0)

    accounts: Optional[Annotated[list[JournalEntryAccountCreate], Field(min_length=1)]] = None



    @field_validator("title", "cheque_no", "bill_no", "pay_to_recd_from", "mode_of_payment", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class JournalEntryRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    naming_series: str

    title: Optional[str] = None

    voucher_type: JournalVoucherType

    posting_date: dt.date

    cheque_no: Optional[str] = None

    cheque_date: Optional[dt.date] = None

    user_remark: Optional[str] = None

    remark: Optional[str] = None

    bill_no: Optional[str] = None

    bill_date: Optional[dt.date] = None

    due_date: Optional[dt.date] = None

    multi_currency: bool

    pay_to_recd_from: Optional[str] = None

    mode_of_payment: Optional[str] = None

    is_opening: YesNo

    write_off_based_on: WriteOffBasedOn

    write_off_amount: Optional[Decimal] = None

    party_not_required: bool

    custom_remark: bool

    apply_tds: bool

    total_debit: Decimal

    total_credit: Decimal

    difference: Decimal

    accounts: list[JournalEntryAccountRead] = Field(default_factory=list)

    docstatus: int

    amended_from_id: Optional[uuid.UUID] = None

    created_at: datetime

    updated_at: datetime





JournalEntryListResponse = Page[JournalEntryRead]





class JournalEntryStatusResult(ReadSchema):

    id: uuid.UUID

    name: str

    docstatus: int

    total_debit: Decimal

    total_credit: Decimal

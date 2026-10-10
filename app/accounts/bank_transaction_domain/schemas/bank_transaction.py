"""

Pydantic v2 schemas for Bank Transaction.



``status``, ``allocated_amount`` and ``unallocated_amount`` are derived, so they

appear only in ``Read``. ``excluded_fee`` IS accepted on input: upstream

consumes it in ``handle_excluded_fee`` and folds it into ``deposit``/

``withdrawal``/``included_fee``, so it is a genuine write-time input.

"""



from __future__ import annotations



import uuid

import datetime as dt

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.accounts.bank_transaction_domain.models.bank_transaction import (

    BankTransactionStatus,

    NAMING_SERIES,

)

from app.accounts.bank_transaction_payments_domain.schemas.bank_transaction_payments import (

    BankTransactionPaymentCreate,

    BankTransactionPaymentRead,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "BankTransactionCreate",

    "BankTransactionUpdate",

    "BankTransactionRead",

    "BankTransactionListResponse",

    "BankTransactionStatusResult",

]



_STR = Annotated[str, Field(max_length=140)]





class BankTransactionCreate(InputSchema):

    naming_series: _STR = Field(default=NAMING_SERIES)

    date: Optional[dt.date] = None

    bank_account_id: Optional[uuid.UUID] = None

    currency: Optional[_STR] = None



    deposit: Optional[Decimal] = Field(default=None, ge=0)

    withdrawal: Optional[Decimal] = Field(default=None, ge=0)

    included_fee: Optional[Decimal] = Field(default=None, ge=0)

    excluded_fee: Optional[Decimal] = Field(default=None, ge=0)



    description: Optional[str] = None

    reference_number: Optional[_STR] = None

    transaction_id: Optional[_STR] = None

    transaction_type: Optional[_STR] = None



    party_type: Optional[_STR] = None

    party: Optional[_STR] = None



    bank_party_name: Optional[_STR] = None

    bank_party_iban: Optional[_STR] = None

    bank_party_account_number: Optional[_STR] = None



    payment_entries: list[BankTransactionPaymentCreate] = Field(default_factory=list)



    @field_validator(

        "currency", "reference_number", "transaction_id", "transaction_type",

        "party_type", "party", "bank_party_name", "bank_party_iban",

        "bank_party_account_number",

        mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankTransactionUpdate(InputSchema):

    """

    ``bank_account_id`` is absent: the currency guard is resolved against the

    bank account's GL account, so repointing it could retroactively break the

    invariant. Allocations stay editable after submit, mirroring

    ``before_update_after_submit``.

    """



    date: Optional[dt.date] = None

    currency: Optional[_STR] = None



    deposit: Optional[Decimal] = Field(default=None, ge=0)

    withdrawal: Optional[Decimal] = Field(default=None, ge=0)

    included_fee: Optional[Decimal] = Field(default=None, ge=0)

    excluded_fee: Optional[Decimal] = Field(default=None, ge=0)



    description: Optional[str] = None

    reference_number: Optional[_STR] = None

    transaction_id: Optional[_STR] = None

    transaction_type: Optional[_STR] = None



    party_type: Optional[_STR] = None

    party: Optional[_STR] = None



    bank_party_name: Optional[_STR] = None

    bank_party_iban: Optional[_STR] = None

    bank_party_account_number: Optional[_STR] = None



    payment_entries: Optional[list[BankTransactionPaymentCreate]] = None



    @field_validator(

        "currency", "reference_number", "transaction_id", "transaction_type",

        "party_type", "party", "bank_party_name", "bank_party_iban",

        "bank_party_account_number",

        mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankTransactionRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    naming_series: str

    date: Optional[dt.date] = None

    status: BankTransactionStatus

    bank_account_id: Optional[uuid.UUID] = None

    currency: Optional[str] = None

    deposit: Optional[Decimal] = None

    withdrawal: Optional[Decimal] = None

    included_fee: Optional[Decimal] = None

    excluded_fee: Optional[Decimal] = None

    allocated_amount: Optional[Decimal] = None

    unallocated_amount: Optional[Decimal] = None

    description: Optional[str] = None

    reference_number: Optional[str] = None

    transaction_id: Optional[str] = None

    transaction_type: Optional[str] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    bank_party_name: Optional[str] = None

    bank_party_iban: Optional[str] = None

    bank_party_account_number: Optional[str] = None

    is_rule_evaluated: bool

    matched_transaction_rule_id: Optional[uuid.UUID] = None

    payment_entries: list[BankTransactionPaymentRead] = Field(default_factory=list)

    docstatus: int

    amended_from_id: Optional[uuid.UUID] = None

    created_at: dt.datetime

    updated_at: dt.datetime





BankTransactionListResponse = Page[BankTransactionRead]





class BankTransactionStatusResult(ReadSchema):

    """What the lifecycle endpoints return: the docstatus *and* derived status."""



    id: uuid.UUID

    name: str

    docstatus: int

    status: BankTransactionStatus

    allocated_amount: Optional[Decimal] = None

    unallocated_amount: Optional[Decimal] = None

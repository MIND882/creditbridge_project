"""Pydantic v2 schemas for Bank Clearance."""



from __future__ import annotations



import uuid

from datetime import date, datetime

from typing import Annotated, Optional



from pydantic import Field, field_validator, model_validator



from app.accounts.bank_clearance_detail_domain.schemas.bank_clearance_detail import (

    BankClearanceDetailCreate,

    BankClearanceDetailRead,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "BankClearanceCreate",

    "BankClearanceUpdate",

    "BankClearanceRead",

    "BankClearanceListResponse",

    "BankClearanceEntriesResult",

]





class BankClearanceCreate(InputSchema):

    account_id: uuid.UUID

    from_date: date

    to_date: date

    bank_account_id: Optional[uuid.UUID] = None

    account_currency: Optional[Annotated[str, Field(max_length=140)]] = None

    include_reconciled_entries: bool = False

    include_pos_transactions: bool = False

    payment_entries: list[BankClearanceDetailCreate] = Field(default_factory=list)



    @field_validator("account_currency", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)



    @model_validator(mode="after")

    def _range_is_ordered(self) -> "BankClearanceCreate":

        """

        Upstream throws this inside ``get_payment_entries`` ("From Date and To

        Date are Mandatory"); checked at the edge too, since a reversed range

        can only ever return nothing.

        """

        if self.to_date < self.from_date:

            raise ValueError("To Date cannot be before From Date")

        return self





class BankClearanceUpdate(InputSchema):

    """

    ``account_id`` is absent: the entries are fetched for that account, so

    changing it would leave the child rows describing a different account.

    """



    from_date: Optional[date] = None

    to_date: Optional[date] = None

    bank_account_id: Optional[uuid.UUID] = None

    account_currency: Optional[Annotated[str, Field(max_length=140)]] = None

    include_reconciled_entries: Optional[bool] = None

    include_pos_transactions: Optional[bool] = None

    payment_entries: Optional[list[BankClearanceDetailCreate]] = None



    @field_validator("account_currency", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankClearanceRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    account_id: uuid.UUID

    account_currency: Optional[str] = None

    from_date: date

    to_date: date

    bank_account_id: Optional[uuid.UUID] = None

    include_reconciled_entries: bool

    include_pos_transactions: bool

    payment_entries: list[BankClearanceDetailRead] = Field(default_factory=list)

    created_at: datetime

    updated_at: datetime





BankClearanceListResponse = Page[BankClearanceRead]





class BankClearanceEntriesResult(ReadSchema):

    """What the ``get_payment_entries`` endpoint returns for one run."""



    id: uuid.UUID

    name: str

    refreshed: int = Field(description="How many entry rows the run produced")

    payment_entries: list[BankClearanceDetailRead] = Field(default_factory=list)

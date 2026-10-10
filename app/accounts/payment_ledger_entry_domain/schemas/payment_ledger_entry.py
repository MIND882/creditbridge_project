"""Pydantic v2 contracts for Payment Ledger Entry."""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from pydantic import BaseModel, ConfigDict, Field, field_validator



from app.accounts.payment_ledger_entry_domain.models.payment_ledger_entry import PLEAccountType

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import ResultPage



__all__ = [

    "PaymentLedgerEntryCreate",

    "PaymentLedgerEntryUpdate",

    "PaymentLedgerEntryRead",

    "PaymentLedgerEntryListResponse",

    "PaymentLedgerEntryStatusResult",

    "OutstandingRead",

]





class PaymentLedgerEntryBase(BaseModel):

    """Client-supplied fields. Never accepts ``business_id`` or ``docstatus``."""



    posting_date: Optional[date] = Field(default=None)

    account_type: Optional[PLEAccountType] = Field(default=None)

    account_id: Optional[uuid.UUID] = Field(default=None)



    party_type: Optional[str] = Field(default=None, max_length=140)

    party: Optional[str] = Field(default=None, max_length=140)



    voucher_type: Optional[str] = Field(default=None, max_length=140)

    voucher_no: Optional[str] = Field(default=None, max_length=140)



    against_voucher_type: Optional[str] = Field(default=None, max_length=140)

    against_voucher_no: Optional[str] = Field(default=None, max_length=140)



    amount: Optional[Decimal] = Field(default=None)



    account_currency: Optional[str] = Field(default=None, max_length=140)

    amount_in_account_currency: Optional[Decimal] = Field(default=None)



    cost_center_id: Optional[uuid.UUID] = Field(default=None)

    finance_book_id: Optional[uuid.UUID] = Field(default=None)



    project: Optional[str] = Field(default=None, max_length=140)

    due_date: Optional[date] = Field(default=None)

    voucher_detail_no: Optional[str] = Field(default=None, max_length=140)

    remarks: Optional[str] = Field(default=None)





class PaymentLedgerEntryCreate(PaymentLedgerEntryBase, InputSchema):

    """

    A row to write into the party ledger.



    ``docstatus`` is not accepted: entries arrive submitted, because a payment

    ledger row only means something once the voucher behind it is final.

    """



    @field_validator(

        "party_type", "party", "voucher_type", "voucher_no", "against_voucher_type",

        "against_voucher_no", "account_currency", "project", "voucher_detail_no", "remarks",

        mode="before",

    )

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class PaymentLedgerEntryUpdate(InputSchema):

    """

    A partial update. Upstream only ever flips ``delinked`` after the fact --

    writing a row off, or undoing a write-off -- so that is the sole editable

    field here. Changing the amount of a posted ledger row would silently move

    a party's outstanding balance with no voucher behind it.

    """



    delinked: Optional[bool] = Field(default=None)





class PaymentLedgerEntryRead(PaymentLedgerEntryBase, ReadSchema):

    id: uuid.UUID

    name: str

    delinked: bool

    docstatus: int

    amended_from_id: Optional[uuid.UUID] = None



    model_config = ConfigDict(from_attributes=True)





class PaymentLedgerEntryStatusResult(BaseModel):

    id: uuid.UUID

    name: str

    docstatus: int

    delinked: bool





class OutstandingRead(BaseModel):

    """

    A party's running balance -- what Payment Ledger Entry actually exists for.



    ``invoice_outstanding`` narrows to one document; ``party_outstanding`` is

    everything still open for that party across all invoices.

    """



    party_type: Optional[str] = None

    party: Optional[str] = None

    against_voucher_no: Optional[str] = None

    invoice_outstanding: Decimal

    party_outstanding: Decimal





class PaymentLedgerEntryListResponse(BaseModel):

    """Page wrapper."""



    items: list[PaymentLedgerEntryRead]

    total: int

    offset: int

    limit: int



    @classmethod

    def from_result(

        cls, result: ResultPage[object], items: list[PaymentLedgerEntryRead]

    ) -> "PaymentLedgerEntryListResponse":

        return cls(items=items, total=result.total, offset=result.offset, limit=result.limit)

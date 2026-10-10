"""Pydantic v2 schemas for AdvancePaymentLedgerEntry."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "AdvancePaymentLedgerEntryCreate",

    "AdvancePaymentLedgerEntryUpdate",

    "AdvancePaymentLedgerEntryRead",

    "AdvancePaymentLedgerEntryListResponse",

]





class AdvancePaymentLedgerEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    against_voucher_type: Optional[str] = None

    against_voucher_no: Optional[str] = None

    amount: Optional[Decimal] = None

    currency: Optional[str] = None

    event: Optional[str] = None

    delinked: Optional[bool] = None

    base_amount: Optional[Decimal] = None

    exchange_rate: Optional[Decimal] = None





class AdvancePaymentLedgerEntryCreate(AdvancePaymentLedgerEntryBase):

    pass





class AdvancePaymentLedgerEntryUpdate(InputSchema):

    """A partial update."""



    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    against_voucher_type: Optional[str] = None

    against_voucher_no: Optional[str] = None

    amount: Optional[Decimal] = None

    currency: Optional[str] = None

    event: Optional[str] = None

    delinked: Optional[bool] = None

    base_amount: Optional[Decimal] = None

    exchange_rate: Optional[Decimal] = None





class AdvancePaymentLedgerEntryRead(ReadSchema):

    id: uuid.UUID

    name: str

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    against_voucher_type: Optional[str] = None

    against_voucher_no: Optional[str] = None

    amount: Optional[Decimal] = None

    currency: Optional[str] = None

    event: Optional[str] = None

    delinked: bool

    base_amount: Optional[Decimal] = None

    exchange_rate: Optional[Decimal] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





AdvancePaymentLedgerEntryListResponse = Page[AdvancePaymentLedgerEntryRead]

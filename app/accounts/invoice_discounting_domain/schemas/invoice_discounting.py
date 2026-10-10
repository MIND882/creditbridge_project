"""Pydantic v2 schemas for InvoiceDiscounting."""





from __future__ import annotations

from app.accounts.invoice_discounting_domain.models.invoice_discounting import (

    InvoiceDiscountingStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.discounted_invoice_domain.schemas.discounted_invoice import (

    DiscountedInvoiceCreate,

    DiscountedInvoiceRead,

)



__all__ = [

    "InvoiceDiscountingCreate",

    "InvoiceDiscountingUpdate",

    "InvoiceDiscountingRead",

    "InvoiceDiscountingListResponse",

]





class InvoiceDiscountingBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    posting_date: dt.date

    loan_start_date: Optional[dt.date] = None

    loan_period: Optional[int] = None

    loan_end_date: Optional[dt.date] = None

    status: Optional[InvoiceDiscountingStatus] = None

    total_amount: Optional[Decimal] = None

    bank_charges: Optional[Decimal] = None

    short_term_loan_id: uuid.UUID

    bank_account_id: uuid.UUID

    bank_charges_account_id: uuid.UUID

    accounts_receivable_credit_id: uuid.UUID

    accounts_receivable_discounted_id: uuid.UUID

    accounts_receivable_unpaid_id: uuid.UUID

    amended_from: Optional[str] = None



    invoices: list[DiscountedInvoiceCreate] = []





class InvoiceDiscountingCreate(InvoiceDiscountingBase):

    pass





class InvoiceDiscountingUpdate(InputSchema):

    """A partial update."""



    posting_date: Optional[dt.date] = None

    loan_start_date: Optional[dt.date] = None

    loan_period: Optional[int] = None

    loan_end_date: Optional[dt.date] = None

    status: Optional[InvoiceDiscountingStatus] = None

    total_amount: Optional[Decimal] = None

    bank_charges: Optional[Decimal] = None

    short_term_loan_id: Optional[uuid.UUID] = None

    bank_account_id: Optional[uuid.UUID] = None

    bank_charges_account_id: Optional[uuid.UUID] = None

    accounts_receivable_credit_id: Optional[uuid.UUID] = None

    accounts_receivable_discounted_id: Optional[uuid.UUID] = None

    accounts_receivable_unpaid_id: Optional[uuid.UUID] = None

    amended_from: Optional[str] = None

    invoices: Optional[list[DiscountedInvoiceCreate]] = None





class InvoiceDiscountingRead(ReadSchema):

    id: uuid.UUID

    name: str

    posting_date: dt.date

    loan_start_date: Optional[dt.date] = None

    loan_period: Optional[int] = None

    loan_end_date: Optional[dt.date] = None

    status: Optional[InvoiceDiscountingStatus] = None

    total_amount: Optional[Decimal] = None

    bank_charges: Optional[Decimal] = None

    short_term_loan_id: uuid.UUID

    bank_account_id: uuid.UUID

    bank_charges_account_id: uuid.UUID

    accounts_receivable_credit_id: uuid.UUID

    accounts_receivable_discounted_id: uuid.UUID

    accounts_receivable_unpaid_id: uuid.UUID

    amended_from: Optional[str] = None

    invoices: list[DiscountedInvoiceRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





InvoiceDiscountingListResponse = Page[InvoiceDiscountingRead]

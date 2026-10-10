"""Pydantic v2 schemas for PaymentReconciliation."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.accounts.payment_reconciliation_payment_domain.schemas.payment_reconciliation_payment import (

    PaymentReconciliationPaymentCreate,

    PaymentReconciliationPaymentRead,

)

from app.accounts.payment_reconciliation_invoice_domain.schemas.payment_reconciliation_invoice import (

    PaymentReconciliationInvoiceCreate,

    PaymentReconciliationInvoiceRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.cashier_closing_payments_domain.schemas.cashier_closing_payments import (

    CashierClosingPaymentsCreate,

    CashierClosingPaymentsRead,

)

from app.accounts.discounted_invoice_domain.schemas.discounted_invoice import (

    DiscountedInvoiceCreate,

    DiscountedInvoiceRead,

)

from app.accounts.payment_reconciliation_allocation_domain.schemas.payment_reconciliation_allocation import (

    PaymentReconciliationAllocationCreate,

    PaymentReconciliationAllocationRead,

)



__all__ = [

    "PaymentReconciliationCreate",

    "PaymentReconciliationUpdate",

    "PaymentReconciliationRead",

    "PaymentReconciliationListResponse",

]





class PaymentReconciliationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    party_type: str

    party: Optional[str] = None

    receivable_payable_account_id: uuid.UUID

    bank_cash_account_id: Optional[uuid.UUID] = None

    from_invoice_date: Optional[dt.date] = None

    to_invoice_date: Optional[dt.date] = None

    minimum_invoice_amount: Optional[Decimal] = None

    invoice_limit: Optional[int] = None

    from_payment_date: Optional[dt.date] = None

    to_payment_date: Optional[dt.date] = None

    minimum_payment_amount: Optional[Decimal] = None

    maximum_payment_amount: Optional[Decimal] = None

    payment_limit: Optional[int] = None

    maximum_invoice_amount: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    default_advance_account_id: Optional[uuid.UUID] = None

    invoice_name: Optional[str] = None

    payment_name: Optional[str] = None



    payments: list[PaymentReconciliationPaymentCreate] = []



    invoices: list[PaymentReconciliationInvoiceCreate] = []



    allocation: list[PaymentReconciliationAllocationCreate] = []





class PaymentReconciliationCreate(PaymentReconciliationBase):

    pass





class PaymentReconciliationUpdate(InputSchema):

    """A partial update."""



    party_type: Optional[str] = None

    party: Optional[str] = None

    receivable_payable_account_id: Optional[uuid.UUID] = None

    bank_cash_account_id: Optional[uuid.UUID] = None

    from_invoice_date: Optional[dt.date] = None

    to_invoice_date: Optional[dt.date] = None

    minimum_invoice_amount: Optional[Decimal] = None

    invoice_limit: Optional[int] = None

    from_payment_date: Optional[dt.date] = None

    to_payment_date: Optional[dt.date] = None

    minimum_payment_amount: Optional[Decimal] = None

    maximum_payment_amount: Optional[Decimal] = None

    payment_limit: Optional[int] = None

    maximum_invoice_amount: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    default_advance_account_id: Optional[uuid.UUID] = None

    invoice_name: Optional[str] = None

    payment_name: Optional[str] = None

    payments: Optional[list[PaymentReconciliationPaymentCreate]] = None

    invoices: Optional[list[PaymentReconciliationInvoiceCreate]] = None

    allocation: Optional[list[PaymentReconciliationAllocationCreate]] = None





class PaymentReconciliationRead(ReadSchema):

    id: uuid.UUID

    name: str

    party_type: str

    party: Optional[str] = None

    receivable_payable_account_id: uuid.UUID

    bank_cash_account_id: Optional[uuid.UUID] = None

    from_invoice_date: Optional[dt.date] = None

    to_invoice_date: Optional[dt.date] = None

    minimum_invoice_amount: Optional[Decimal] = None

    invoice_limit: Optional[int] = None

    from_payment_date: Optional[dt.date] = None

    to_payment_date: Optional[dt.date] = None

    minimum_payment_amount: Optional[Decimal] = None

    maximum_payment_amount: Optional[Decimal] = None

    payment_limit: Optional[int] = None

    maximum_invoice_amount: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    default_advance_account_id: Optional[uuid.UUID] = None

    invoice_name: Optional[str] = None

    payment_name: Optional[str] = None

    payments: list[PaymentReconciliationPaymentRead] = []

    invoices: list[PaymentReconciliationInvoiceRead] = []

    allocation: list[PaymentReconciliationAllocationRead] = []





PaymentReconciliationListResponse = Page[PaymentReconciliationRead]

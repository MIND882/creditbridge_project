"""Pydantic v2 schemas for ProcessPaymentReconciliation."""





from __future__ import annotations

from app.accounts.process_payment_reconciliation_domain.models.process_payment_reconciliation import (

    ProcessPaymentReconciliationStatus,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProcessPaymentReconciliationCreate",

    "ProcessPaymentReconciliationUpdate",

    "ProcessPaymentReconciliationRead",

    "ProcessPaymentReconciliationListResponse",

]





class ProcessPaymentReconciliationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    status: Optional[ProcessPaymentReconciliationStatus] = None

    party_type: str

    party: Optional[str] = None

    receivable_payable_account_id: uuid.UUID

    from_invoice_date: Optional[dt.date] = None

    to_invoice_date: Optional[dt.date] = None

    from_payment_date: Optional[dt.date] = None

    to_payment_date: Optional[dt.date] = None

    cost_center_id: Optional[uuid.UUID] = None

    bank_cash_account_id: Optional[uuid.UUID] = None

    error_log: Optional[str] = None

    amended_from: Optional[str] = None

    default_advance_account_id: Optional[uuid.UUID] = None





class ProcessPaymentReconciliationCreate(ProcessPaymentReconciliationBase):

    pass





class ProcessPaymentReconciliationUpdate(InputSchema):

    """A partial update."""



    status: Optional[ProcessPaymentReconciliationStatus] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    receivable_payable_account_id: Optional[uuid.UUID] = None

    from_invoice_date: Optional[dt.date] = None

    to_invoice_date: Optional[dt.date] = None

    from_payment_date: Optional[dt.date] = None

    to_payment_date: Optional[dt.date] = None

    cost_center_id: Optional[uuid.UUID] = None

    bank_cash_account_id: Optional[uuid.UUID] = None

    error_log: Optional[str] = None

    amended_from: Optional[str] = None

    default_advance_account_id: Optional[uuid.UUID] = None





class ProcessPaymentReconciliationRead(ReadSchema):

    id: uuid.UUID

    name: str

    status: Optional[ProcessPaymentReconciliationStatus] = None

    party_type: str

    party: Optional[str] = None

    receivable_payable_account_id: uuid.UUID

    from_invoice_date: Optional[dt.date] = None

    to_invoice_date: Optional[dt.date] = None

    from_payment_date: Optional[dt.date] = None

    to_payment_date: Optional[dt.date] = None

    cost_center_id: Optional[uuid.UUID] = None

    bank_cash_account_id: Optional[uuid.UUID] = None

    error_log: Optional[str] = None

    amended_from: Optional[str] = None

    default_advance_account_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





ProcessPaymentReconciliationListResponse = Page[ProcessPaymentReconciliationRead]

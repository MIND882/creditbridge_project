"""Pydantic v2 schemas for POSClosingEntry."""





from __future__ import annotations

from app.accounts.pos_closing_entry_domain.models.pos_closing_entry import (

    POSClosingEntryStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.pos_closing_entry_detail_domain.schemas.pos_closing_entry_detail import (

    POSClosingEntryDetailCreate,

    POSClosingEntryDetailRead,

)

from app.accounts.pos_closing_entry_taxes_domain.schemas.pos_closing_entry_taxes import (

    POSClosingEntryTaxesCreate,

    POSClosingEntryTaxesRead,

)

from app.accounts.pos_invoice_reference_domain.schemas.pos_invoice_reference import (

    POSInvoiceReferenceCreate,

    POSInvoiceReferenceRead,

)

from app.accounts.sales_invoice_reference_domain.schemas.sales_invoice_reference import (

    SalesInvoiceReferenceCreate,

    SalesInvoiceReferenceRead,

)



__all__ = [

    "POSClosingEntryCreate",

    "POSClosingEntryUpdate",

    "POSClosingEntryRead",

    "POSClosingEntryListResponse",

]





class POSClosingEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    period_start_date: Optional[dt.datetime] = None

    period_end_date: Optional[dt.datetime] = None

    posting_date: dt.date

    pos_profile: str

    user: str

    grand_total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_quantity: Optional[Decimal] = None

    amended_from: Optional[str] = None

    pos_opening_entry: str

    status: Optional[POSClosingEntryStatus] = None

    error_message: Optional[str] = None

    posting_time: Optional[dt.time] = None

    total_taxes_and_charges: Optional[Decimal] = None



    payment_reconciliation: list[POSClosingEntryDetailCreate] = []



    taxes: list[POSClosingEntryTaxesCreate] = []



    pos_invoices: list[POSInvoiceReferenceCreate] = []



    sales_invoices: list[SalesInvoiceReferenceCreate] = []





class POSClosingEntryCreate(POSClosingEntryBase):

    pass





class POSClosingEntryUpdate(InputSchema):

    """A partial update."""



    period_start_date: Optional[dt.datetime] = None

    period_end_date: Optional[dt.datetime] = None

    posting_date: Optional[dt.date] = None

    pos_profile: Optional[str] = None

    user: Optional[str] = None

    grand_total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_quantity: Optional[Decimal] = None

    amended_from: Optional[str] = None

    pos_opening_entry: Optional[str] = None

    status: Optional[POSClosingEntryStatus] = None

    error_message: Optional[str] = None

    posting_time: Optional[dt.time] = None

    total_taxes_and_charges: Optional[Decimal] = None

    payment_reconciliation: Optional[list[POSClosingEntryDetailCreate]] = None

    taxes: Optional[list[POSClosingEntryTaxesCreate]] = None

    pos_invoices: Optional[list[POSInvoiceReferenceCreate]] = None

    sales_invoices: Optional[list[SalesInvoiceReferenceCreate]] = None





class POSClosingEntryRead(ReadSchema):

    id: uuid.UUID

    name: str

    period_start_date: Optional[dt.datetime] = None

    period_end_date: Optional[dt.datetime] = None

    posting_date: dt.date

    pos_profile: str

    user: str

    grand_total: Optional[Decimal] = None

    net_total: Optional[Decimal] = None

    total_quantity: Optional[Decimal] = None

    amended_from: Optional[str] = None

    pos_opening_entry: str

    status: Optional[POSClosingEntryStatus] = None

    error_message: Optional[str] = None

    posting_time: Optional[dt.time] = None

    total_taxes_and_charges: Optional[Decimal] = None

    payment_reconciliation: list[POSClosingEntryDetailRead] = []

    taxes: list[POSClosingEntryTaxesRead] = []

    pos_invoices: list[POSInvoiceReferenceRead] = []

    sales_invoices: list[SalesInvoiceReferenceRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





POSClosingEntryListResponse = Page[POSClosingEntryRead]

"""Pydantic v2 schemas for POSInvoiceMergeLog."""





from __future__ import annotations

from app.accounts.pos_invoice_merge_log_domain.models.pos_invoice_merge_log import (

    POSInvoiceMergeLogMergeInvoicesBasedOn,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.pos_invoice_reference_domain.schemas.pos_invoice_reference import (

    POSInvoiceReferenceCreate,

    POSInvoiceReferenceRead,

)



__all__ = [

    "POSInvoiceMergeLogCreate",

    "POSInvoiceMergeLogUpdate",

    "POSInvoiceMergeLogRead",

    "POSInvoiceMergeLogListResponse",

]





class POSInvoiceMergeLogBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    posting_date: dt.date

    customer: str

    amended_from: Optional[str] = None

    consolidated_invoice: Optional[str] = None

    consolidated_credit_note: Optional[str] = None

    pos_closing_entry: Optional[str] = None

    merge_invoices_based_on: POSInvoiceMergeLogMergeInvoicesBasedOn

    customer_group: Optional[str] = None

    posting_time: Optional[dt.time] = None



    pos_invoices: list[POSInvoiceReferenceCreate] = []





class POSInvoiceMergeLogCreate(POSInvoiceMergeLogBase):

    pass





class POSInvoiceMergeLogUpdate(InputSchema):

    """A partial update."""



    posting_date: Optional[dt.date] = None

    customer: Optional[str] = None

    amended_from: Optional[str] = None

    consolidated_invoice: Optional[str] = None

    consolidated_credit_note: Optional[str] = None

    pos_closing_entry: Optional[str] = None

    merge_invoices_based_on: Optional[POSInvoiceMergeLogMergeInvoicesBasedOn] = None

    customer_group: Optional[str] = None

    posting_time: Optional[dt.time] = None

    pos_invoices: Optional[list[POSInvoiceReferenceCreate]] = None





class POSInvoiceMergeLogRead(ReadSchema):

    id: uuid.UUID

    name: str

    posting_date: dt.date

    customer: str

    amended_from: Optional[str] = None

    consolidated_invoice: Optional[str] = None

    consolidated_credit_note: Optional[str] = None

    pos_closing_entry: Optional[str] = None

    merge_invoices_based_on: POSInvoiceMergeLogMergeInvoicesBasedOn

    customer_group: Optional[str] = None

    posting_time: Optional[dt.time] = None

    pos_invoices: list[POSInvoiceReferenceRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





POSInvoiceMergeLogListResponse = Page[POSInvoiceMergeLogRead]

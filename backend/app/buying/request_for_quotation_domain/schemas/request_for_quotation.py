"""Pydantic v2 schemas for RequestForQuotation."""





from __future__ import annotations

from app.buying.request_for_quotation_domain.models.request_for_quotation import (

    RequestForQuotationNamingSeries,

    RequestForQuotationStatus,

)

from typing import Optional

import datetime as dt

import uuid



from app.buying.request_for_quotation_supplier_domain.schemas.request_for_quotation_supplier import (

    RequestForQuotationSupplierCreate,

    RequestForQuotationSupplierRead,

)

from app.buying.request_for_quotation_item_domain.schemas.request_for_quotation_item import (

    RequestForQuotationItemCreate,

    RequestForQuotationItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "RequestForQuotationCreate",

    "RequestForQuotationUpdate",

    "RequestForQuotationRead",

    "RequestForQuotationListResponse",

]





class RequestForQuotationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: RequestForQuotationNamingSeries

    company: str

    vendor_id: Optional[uuid.UUID] = None

    transaction_date: dt.date

    email_template: Optional[str] = None

    message_for_supplier: Optional[str] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    select_print_heading: Optional[str] = None

    letter_head: Optional[str] = None

    opportunity: Optional[str] = None

    status: RequestForQuotationStatus

    amended_from_id: Optional[uuid.UUID] = None

    schedule_date: Optional[dt.date] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    send_attached_files: Optional[bool] = None

    send_document_print: Optional[bool] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    has_unit_price_items: Optional[bool] = None

    subject: str

    mfs_html: Optional[str] = None

    use_html: Optional[bool] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    title: Optional[str] = None

    suppliers: list[RequestForQuotationSupplierCreate] = []

    items: list[RequestForQuotationItemCreate] = []





class RequestForQuotationCreate(RequestForQuotationBase):

    pass





class RequestForQuotationUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[RequestForQuotationNamingSeries] = None

    company: Optional[str] = None

    vendor_id: Optional[uuid.UUID] = None

    transaction_date: Optional[dt.date] = None

    email_template: Optional[str] = None

    message_for_supplier: Optional[str] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    select_print_heading: Optional[str] = None

    letter_head: Optional[str] = None

    opportunity: Optional[str] = None

    status: Optional[RequestForQuotationStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    schedule_date: Optional[dt.date] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    send_attached_files: Optional[bool] = None

    send_document_print: Optional[bool] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    has_unit_price_items: Optional[bool] = None

    subject: Optional[str] = None

    mfs_html: Optional[str] = None

    use_html: Optional[bool] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    title: Optional[str] = None

    suppliers: Optional[list[RequestForQuotationSupplierCreate]] = None

    items: Optional[list[RequestForQuotationItemCreate]] = None





class RequestForQuotationRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[RequestForQuotationNamingSeries] = None

    company: str

    vendor_id: Optional[uuid.UUID] = None

    transaction_date: Optional[dt.date] = None

    email_template: Optional[str] = None

    message_for_supplier: Optional[str] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    select_print_heading: Optional[str] = None

    letter_head: Optional[str] = None

    opportunity: Optional[str] = None

    status: Optional[RequestForQuotationStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    schedule_date: Optional[dt.date] = None

    incoterm: Optional[str] = None

    named_place: Optional[str] = None

    send_attached_files: Optional[bool] = None

    send_document_print: Optional[bool] = None

    billing_address: Optional[str] = None

    billing_address_display: Optional[str] = None

    has_unit_price_items: Optional[bool] = None

    subject: str

    mfs_html: Optional[str] = None

    use_html: Optional[bool] = None

    shipping_address: Optional[str] = None

    shipping_address_display: Optional[str] = None

    title: Optional[str] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    suppliers: list[RequestForQuotationSupplierRead] = []

    items: list[RequestForQuotationItemRead] = []





RequestForQuotationListResponse = Page[RequestForQuotationRead]

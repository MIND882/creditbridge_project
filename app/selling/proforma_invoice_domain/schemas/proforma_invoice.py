"""Pydantic v2 schemas for ProformaInvoice."""





from __future__ import annotations

from app.selling.proforma_invoice_domain.models.proforma_invoice import (

    ProformaInvoiceNamingSeries,

    ProformaInvoiceBasedOn,

    ProformaInvoiceStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.selling.proforma_invoice_item_domain.schemas.proforma_invoice_item import (

    ProformaInvoiceItemCreate,

    ProformaInvoiceItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProformaInvoiceCreate",

    "ProformaInvoiceUpdate",

    "ProformaInvoiceRead",

    "ProformaInvoiceListResponse",

]





class ProformaInvoiceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: ProformaInvoiceNamingSeries

    sales_order_id: uuid.UUID

    customer_id: Optional[uuid.UUID] = None

    customer_name: Optional[str] = None

    company: str

    proforma_date: dt.date

    currency: Optional[str] = None

    based_on: Optional[ProformaInvoiceBasedOn] = None

    hide_item_qty: Optional[bool] = None

    total_qty: Optional[Decimal] = None

    grand_total: Optional[Decimal] = None

    print_format: Optional[str] = None

    letter_head: Optional[str] = None

    proforma_pdf: Optional[str] = None

    status: Optional[ProformaInvoiceStatus] = None

    sent_on: Optional[dt.datetime] = None

    emailed_to: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    items: list[ProformaInvoiceItemCreate] = []





class ProformaInvoiceCreate(ProformaInvoiceBase):

    pass





class ProformaInvoiceUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[ProformaInvoiceNamingSeries] = None

    sales_order_id: Optional[uuid.UUID] = None

    customer_id: Optional[uuid.UUID] = None

    customer_name: Optional[str] = None

    company: Optional[str] = None

    proforma_date: Optional[dt.date] = None

    currency: Optional[str] = None

    based_on: Optional[ProformaInvoiceBasedOn] = None

    hide_item_qty: Optional[bool] = None

    total_qty: Optional[Decimal] = None

    grand_total: Optional[Decimal] = None

    print_format: Optional[str] = None

    letter_head: Optional[str] = None

    proforma_pdf: Optional[str] = None

    status: Optional[ProformaInvoiceStatus] = None

    sent_on: Optional[dt.datetime] = None

    emailed_to: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    items: Optional[list[ProformaInvoiceItemCreate]] = None





class ProformaInvoiceRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[ProformaInvoiceNamingSeries] = None

    sales_order_id: Optional[uuid.UUID] = None

    customer_id: Optional[uuid.UUID] = None

    customer_name: Optional[str] = None

    company: str

    proforma_date: Optional[dt.date] = None

    currency: Optional[str] = None

    based_on: Optional[ProformaInvoiceBasedOn] = None

    hide_item_qty: Optional[bool] = None

    total_qty: Optional[Decimal] = None

    grand_total: Optional[Decimal] = None

    print_format: Optional[str] = None

    letter_head: Optional[str] = None

    proforma_pdf: Optional[str] = None

    status: Optional[ProformaInvoiceStatus] = None

    sent_on: Optional[dt.datetime] = None

    emailed_to: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    items: list[ProformaInvoiceItemRead] = []





ProformaInvoiceListResponse = Page[ProformaInvoiceRead]

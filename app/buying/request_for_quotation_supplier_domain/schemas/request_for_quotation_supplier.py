"""Pydantic v2 schemas for RequestForQuotationSupplier."""





from __future__ import annotations

from app.buying.request_for_quotation_supplier_domain.models.request_for_quotation_supplier import (

    RequestForQuotationSupplierQuoteStatus,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "RequestForQuotationSupplierCreate",

    "RequestForQuotationSupplierRead",

    "RequestForQuotationSupplierListResponse",

]





class RequestForQuotationSupplierBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    send_email: Optional[bool] = None

    email_sent: Optional[bool] = None

    supplier_id: uuid.UUID

    contact: Optional[str] = None

    quote_status: Optional[RequestForQuotationSupplierQuoteStatus] = None

    supplier_name: Optional[str] = None

    email_id: Optional[str] = None





class RequestForQuotationSupplierCreate(RequestForQuotationSupplierBase):

    pass





class RequestForQuotationSupplierUpdate(InputSchema):

    """A partial update."""



    send_email: Optional[bool] = None

    email_sent: Optional[bool] = None

    supplier_id: Optional[uuid.UUID] = None

    contact: Optional[str] = None

    quote_status: Optional[RequestForQuotationSupplierQuoteStatus] = None

    supplier_name: Optional[str] = None

    email_id: Optional[str] = None





class RequestForQuotationSupplierRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    send_email: Optional[bool] = None

    email_sent: Optional[bool] = None

    supplier_id: Optional[uuid.UUID] = None

    contact: Optional[str] = None

    quote_status: Optional[RequestForQuotationSupplierQuoteStatus] = None

    supplier_name: Optional[str] = None

    email_id: Optional[str] = None





RequestForQuotationSupplierListResponse = Page[RequestForQuotationSupplierRead]

"""Pydantic v2 schemas for LandedCostVendorInvoice."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LandedCostVendorInvoiceCreate",

    "LandedCostVendorInvoiceRead",

    "LandedCostVendorInvoiceListResponse",

]





class LandedCostVendorInvoiceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    vendor_invoice_id: Optional[uuid.UUID] = None

    amount: Optional[Decimal] = None





class LandedCostVendorInvoiceCreate(LandedCostVendorInvoiceBase):

    pass





class LandedCostVendorInvoiceUpdate(InputSchema):

    """A partial update."""



    vendor_invoice_id: Optional[uuid.UUID] = None

    amount: Optional[Decimal] = None





class LandedCostVendorInvoiceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    vendor_invoice_id: Optional[uuid.UUID] = None

    amount: Optional[Decimal] = None





LandedCostVendorInvoiceListResponse = Page[LandedCostVendorInvoiceRead]

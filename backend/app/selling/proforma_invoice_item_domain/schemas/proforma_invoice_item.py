"""Pydantic v2 schemas for ProformaInvoiceItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProformaInvoiceItemCreate",

    "ProformaInvoiceItemRead",

    "ProformaInvoiceItemListResponse",

]





class ProformaInvoiceItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    qty: Decimal

    uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    so_detail: Optional[str] = None





class ProformaInvoiceItemCreate(ProformaInvoiceItemBase):

    pass





class ProformaInvoiceItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    so_detail: Optional[str] = None





class ProformaInvoiceItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    qty: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    so_detail: Optional[str] = None





ProformaInvoiceItemListResponse = Page[ProformaInvoiceItemRead]

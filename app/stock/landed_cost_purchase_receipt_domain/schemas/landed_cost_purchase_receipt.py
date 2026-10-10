"""Pydantic v2 schemas for LandedCostPurchaseReceipt."""





from __future__ import annotations

from app.stock.landed_cost_purchase_receipt_domain.models.landed_cost_purchase_receipt import (

    LandedCostPurchaseReceiptReceiptDocumentType,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LandedCostPurchaseReceiptCreate",

    "LandedCostPurchaseReceiptRead",

    "LandedCostPurchaseReceiptListResponse",

]





class LandedCostPurchaseReceiptBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    receipt_document_type: LandedCostPurchaseReceiptReceiptDocumentType

    receipt_document: str

    supplier: Optional[str] = None

    posting_date: Optional[dt.date] = None

    grand_total: Optional[Decimal] = None





class LandedCostPurchaseReceiptCreate(LandedCostPurchaseReceiptBase):

    pass





class LandedCostPurchaseReceiptUpdate(InputSchema):

    """A partial update."""



    receipt_document_type: Optional[LandedCostPurchaseReceiptReceiptDocumentType] = None

    receipt_document: Optional[str] = None

    supplier: Optional[str] = None

    posting_date: Optional[dt.date] = None

    grand_total: Optional[Decimal] = None





class LandedCostPurchaseReceiptRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    receipt_document_type: Optional[LandedCostPurchaseReceiptReceiptDocumentType] = None

    receipt_document: str

    supplier: Optional[str] = None

    posting_date: Optional[dt.date] = None

    grand_total: Optional[Decimal] = None





LandedCostPurchaseReceiptListResponse = Page[LandedCostPurchaseReceiptRead]

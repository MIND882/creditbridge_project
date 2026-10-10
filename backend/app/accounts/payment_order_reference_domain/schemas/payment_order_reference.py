"""Pydantic v2 schemas for PaymentOrderReference."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PaymentOrderReferenceCreate",

    "PaymentOrderReferenceRead",

    "PaymentOrderReferenceListResponse",

]





class PaymentOrderReferenceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    reference_doctype: str

    reference_name: Optional[str] = None

    amount: Optional[Decimal] = None

    supplier: Optional[str] = None

    payment_request: Optional[str] = None

    mode_of_payment_id: Optional[uuid.UUID] = None

    bank_account_id: uuid.UUID

    account_id: Optional[uuid.UUID] = None

    payment_reference: Optional[str] = None





class PaymentOrderReferenceCreate(PaymentOrderReferenceBase):

    """Accepted only nested inside the parent payload."""

    pass





class PaymentOrderReferenceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    reference_doctype: str

    reference_name: Optional[str] = None

    amount: Decimal

    supplier: Optional[str] = None

    payment_request: Optional[str] = None

    mode_of_payment_id: Optional[uuid.UUID] = None

    bank_account_id: uuid.UUID

    account_id: Optional[uuid.UUID] = None

    payment_reference: Optional[str] = None





PaymentOrderReferenceListResponse = Page[PaymentOrderReferenceRead]

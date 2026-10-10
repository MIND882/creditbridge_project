"""Pydantic v2 schemas for UnreconcilePaymentEntries."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "UnreconcilePaymentEntriesCreate",

    "UnreconcilePaymentEntriesRead",

    "UnreconcilePaymentEntriesListResponse",

]





class UnreconcilePaymentEntriesBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    reference_name: Optional[str] = None

    allocated_amount: Optional[Decimal] = None

    unlinked: Optional[bool] = None

    reference_doctype: Optional[str] = None

    account: Optional[str] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    account_currency: Optional[str] = None





class UnreconcilePaymentEntriesCreate(UnreconcilePaymentEntriesBase):

    """Accepted only nested inside the parent payload."""

    pass





class UnreconcilePaymentEntriesRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    reference_name: Optional[str] = None

    allocated_amount: Optional[Decimal] = None

    unlinked: bool

    reference_doctype: Optional[str] = None

    account: Optional[str] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    account_currency: Optional[str] = None





UnreconcilePaymentEntriesListResponse = Page[UnreconcilePaymentEntriesRead]

"""Pydantic v2 schemas for POSClosingEntryDetail."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "POSClosingEntryDetailCreate",

    "POSClosingEntryDetailRead",

    "POSClosingEntryDetailListResponse",

]





class POSClosingEntryDetailBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    mode_of_payment_id: uuid.UUID

    expected_amount: Optional[Decimal] = None

    difference: Optional[Decimal] = None

    opening_amount: Optional[Decimal] = None

    closing_amount: Optional[Decimal] = None





class POSClosingEntryDetailCreate(POSClosingEntryDetailBase):

    """Accepted only nested inside the parent payload."""

    pass





class POSClosingEntryDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    mode_of_payment_id: uuid.UUID

    expected_amount: Optional[Decimal] = None

    difference: Optional[Decimal] = None

    opening_amount: Decimal

    closing_amount: Decimal





POSClosingEntryDetailListResponse = Page[POSClosingEntryDetailRead]

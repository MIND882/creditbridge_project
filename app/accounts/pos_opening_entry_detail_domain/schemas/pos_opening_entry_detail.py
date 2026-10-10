"""Pydantic v2 schemas for POSOpeningEntryDetail."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "POSOpeningEntryDetailCreate",

    "POSOpeningEntryDetailRead",

    "POSOpeningEntryDetailListResponse",

]





class POSOpeningEntryDetailBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    mode_of_payment_id: uuid.UUID

    opening_amount: Optional[Decimal] = None





class POSOpeningEntryDetailCreate(POSOpeningEntryDetailBase):

    """Accepted only nested inside the parent payload."""

    pass





class POSOpeningEntryDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    mode_of_payment_id: uuid.UUID

    opening_amount: Decimal





POSOpeningEntryDetailListResponse = Page[POSOpeningEntryDetailRead]

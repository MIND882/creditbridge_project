"""Pydantic v2 schemas for POSClosingEntryTaxes."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "POSClosingEntryTaxesCreate",

    "POSClosingEntryTaxesRead",

    "POSClosingEntryTaxesListResponse",

]





class POSClosingEntryTaxesBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    amount: Optional[Decimal] = None

    account_head_id: Optional[uuid.UUID] = None





class POSClosingEntryTaxesCreate(POSClosingEntryTaxesBase):

    """Accepted only nested inside the parent payload."""

    pass





class POSClosingEntryTaxesRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    amount: Optional[Decimal] = None

    account_head_id: Optional[uuid.UUID] = None





POSClosingEntryTaxesListResponse = Page[POSClosingEntryTaxesRead]

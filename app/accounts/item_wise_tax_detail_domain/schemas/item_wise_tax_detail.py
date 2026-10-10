"""

Pydantic v2 contracts for ItemWiseTaxDetail.



An orphan child table: upstream's parents are Sales Invoice and Purchase Invoice,

neither converted. So the API is read-only -- the rows are written by an invoice

when it submits.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["ItemWiseTaxDetailCreate", "ItemWiseTaxDetailRead", "ItemWiseTaxDetailListResponse"]





class ItemWiseTaxDetailCreate(InputSchema):

    """Accepted only nested inside a parent invoice payload, once converted."""



    item_row: str

    tax_row: str

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    taxable_amount: Optional[Decimal] = None





class ItemWiseTaxDetailRead(ReadSchema):

    id: uuid.UUID

    item_row: str

    tax_row: str

    rate: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    taxable_amount: Optional[Decimal] = None





ItemWiseTaxDetailListResponse = Page[ItemWiseTaxDetailRead]

"""Pydantic v2 schemas for ItemTaxTemplateDetail (child table, read-only API)."""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemTaxTemplateDetailCreate",

    "ItemTaxTemplateDetailRead",

    "ItemTaxTemplateDetailListResponse",

]





class ItemTaxTemplateDetailCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    tax_type_id: uuid.UUID

    tax_rate: Optional[Decimal] = None

    not_applicable: Optional[bool] = False





class ItemTaxTemplateDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    tax_type_id: Optional[uuid.UUID] = None

    tax_rate: Optional[Decimal] = None

    not_applicable: bool





ItemTaxTemplateDetailListResponse = Page[ItemTaxTemplateDetailRead]

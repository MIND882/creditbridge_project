"""Pydantic v2 schemas for ItemTax."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemTaxCreate",

    "ItemTaxRead",

    "ItemTaxListResponse",

]





class ItemTaxBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_tax_template_id: uuid.UUID

    tax_category_id: Optional[uuid.UUID] = None

    valid_from: Optional[dt.date] = None

    maximum_net_rate: Optional[Decimal] = None

    minimum_net_rate: Optional[Decimal] = None





class ItemTaxCreate(ItemTaxBase):

    pass





class ItemTaxUpdate(InputSchema):

    """A partial update."""



    item_tax_template_id: Optional[uuid.UUID] = None

    tax_category_id: Optional[uuid.UUID] = None

    valid_from: Optional[dt.date] = None

    maximum_net_rate: Optional[Decimal] = None

    minimum_net_rate: Optional[Decimal] = None





class ItemTaxRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_tax_template_id: Optional[uuid.UUID] = None

    tax_category_id: Optional[uuid.UUID] = None

    valid_from: Optional[dt.date] = None

    maximum_net_rate: Optional[Decimal] = None

    minimum_net_rate: Optional[Decimal] = None





ItemTaxListResponse = Page[ItemTaxRead]

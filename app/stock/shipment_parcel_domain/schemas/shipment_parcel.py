"""Pydantic v2 schemas for ShipmentParcel."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ShipmentParcelCreate",

    "ShipmentParcelRead",

    "ShipmentParcelListResponse",

]





class ShipmentParcelBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    length: Optional[Decimal] = None

    width: Optional[Decimal] = None

    height: Optional[Decimal] = None

    weight: Decimal

    count: int





class ShipmentParcelCreate(ShipmentParcelBase):

    pass





class ShipmentParcelUpdate(InputSchema):

    """A partial update."""



    length: Optional[Decimal] = None

    width: Optional[Decimal] = None

    height: Optional[Decimal] = None

    weight: Optional[Decimal] = None

    count: Optional[int] = None





class ShipmentParcelRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    length: Optional[Decimal] = None

    width: Optional[Decimal] = None

    height: Optional[Decimal] = None

    weight: Optional[Decimal] = None

    count: Optional[int] = None





ShipmentParcelListResponse = Page[ShipmentParcelRead]

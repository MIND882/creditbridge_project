"""Pydantic v2 schemas for ShipmentParcelTemplate."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ShipmentParcelTemplateCreate",

    "ShipmentParcelTemplateUpdate",

    "ShipmentParcelTemplateRead",

    "ShipmentParcelTemplateListResponse",

]





class ShipmentParcelTemplateBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    length: Decimal

    width: Decimal

    height: Decimal

    weight: Decimal

    parcel_template_name: str





class ShipmentParcelTemplateCreate(ShipmentParcelTemplateBase):

    pass





class ShipmentParcelTemplateUpdate(InputSchema):

    """A partial update."""



    length: Optional[Decimal] = None

    width: Optional[Decimal] = None

    height: Optional[Decimal] = None

    weight: Optional[Decimal] = None

    parcel_template_name: Optional[str] = None





class ShipmentParcelTemplateRead(ReadSchema):

    id: uuid.UUID

    name: str

    length: Optional[Decimal] = None

    width: Optional[Decimal] = None

    height: Optional[Decimal] = None

    weight: Optional[Decimal] = None

    parcel_template_name: str





ShipmentParcelTemplateListResponse = Page[ShipmentParcelTemplateRead]

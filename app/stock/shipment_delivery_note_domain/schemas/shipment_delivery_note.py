"""Pydantic v2 schemas for ShipmentDeliveryNote."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ShipmentDeliveryNoteCreate",

    "ShipmentDeliveryNoteRead",

    "ShipmentDeliveryNoteListResponse",

]





class ShipmentDeliveryNoteBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    delivery_note_id: uuid.UUID

    grand_total: Optional[Decimal] = None





class ShipmentDeliveryNoteCreate(ShipmentDeliveryNoteBase):

    pass





class ShipmentDeliveryNoteUpdate(InputSchema):

    """A partial update."""



    delivery_note_id: Optional[uuid.UUID] = None

    grand_total: Optional[Decimal] = None





class ShipmentDeliveryNoteRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    delivery_note_id: Optional[uuid.UUID] = None

    grand_total: Optional[Decimal] = None





ShipmentDeliveryNoteListResponse = Page[ShipmentDeliveryNoteRead]

"""Pydantic v2 schemas for DeliveryStop."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "DeliveryStopCreate",

    "DeliveryStopRead",

    "DeliveryStopListResponse",

]





class DeliveryStopBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    customer: Optional[str] = None

    address: str

    locked: Optional[bool] = None

    customer_address: Optional[str] = None

    visited: Optional[bool] = None

    delivery_note_id: Optional[uuid.UUID] = None

    grand_total: Optional[Decimal] = None

    contact: Optional[str] = None

    email_sent_to: Optional[str] = None

    customer_contact: Optional[str] = None

    distance: Optional[Decimal] = None

    estimated_arrival: Optional[dt.datetime] = None

    lat: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    lng: Optional[Decimal] = None

    details: Optional[str] = None





class DeliveryStopCreate(DeliveryStopBase):

    pass





class DeliveryStopUpdate(InputSchema):

    """A partial update."""



    customer: Optional[str] = None

    address: Optional[str] = None

    locked: Optional[bool] = None

    customer_address: Optional[str] = None

    visited: Optional[bool] = None

    delivery_note_id: Optional[uuid.UUID] = None

    grand_total: Optional[Decimal] = None

    contact: Optional[str] = None

    email_sent_to: Optional[str] = None

    customer_contact: Optional[str] = None

    distance: Optional[Decimal] = None

    estimated_arrival: Optional[dt.datetime] = None

    lat: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    lng: Optional[Decimal] = None

    details: Optional[str] = None





class DeliveryStopRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    customer: Optional[str] = None

    address: str

    locked: Optional[bool] = None

    customer_address: Optional[str] = None

    visited: Optional[bool] = None

    delivery_note_id: Optional[uuid.UUID] = None

    grand_total: Optional[Decimal] = None

    contact: Optional[str] = None

    email_sent_to: Optional[str] = None

    customer_contact: Optional[str] = None

    distance: Optional[Decimal] = None

    estimated_arrival: Optional[dt.datetime] = None

    lat: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    lng: Optional[Decimal] = None

    details: Optional[str] = None





DeliveryStopListResponse = Page[DeliveryStopRead]

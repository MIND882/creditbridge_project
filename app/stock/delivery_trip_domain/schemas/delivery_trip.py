"""Pydantic v2 schemas for DeliveryTrip."""





from __future__ import annotations

from app.stock.delivery_trip_domain.models.delivery_trip import (

    DeliveryTripNamingSeries,

    DeliveryTripStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.delivery_stop_domain.schemas.delivery_stop import (

    DeliveryStopCreate,

    DeliveryStopRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "DeliveryTripCreate",

    "DeliveryTripUpdate",

    "DeliveryTripRead",

    "DeliveryTripListResponse",

]





class DeliveryTripBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: Optional[DeliveryTripNamingSeries] = None

    company: str

    email_notification_sent: Optional[bool] = None

    driver: Optional[str] = None

    driver_name: Optional[str] = None

    total_distance: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    vehicle: str

    departure_time: dt.datetime

    status: Optional[DeliveryTripStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    driver_address: Optional[str] = None

    driver_email: Optional[str] = None

    employee: Optional[str] = None

    delivery_stops: list[DeliveryStopCreate] = []





class DeliveryTripCreate(DeliveryTripBase):

    pass





class DeliveryTripUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[DeliveryTripNamingSeries] = None

    company: Optional[str] = None

    email_notification_sent: Optional[bool] = None

    driver: Optional[str] = None

    driver_name: Optional[str] = None

    total_distance: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    vehicle: Optional[str] = None

    departure_time: Optional[dt.datetime] = None

    status: Optional[DeliveryTripStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    driver_address: Optional[str] = None

    driver_email: Optional[str] = None

    employee: Optional[str] = None

    delivery_stops: Optional[list[DeliveryStopCreate]] = None





class DeliveryTripRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[DeliveryTripNamingSeries] = None

    company: str

    email_notification_sent: Optional[bool] = None

    driver: Optional[str] = None

    driver_name: Optional[str] = None

    total_distance: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    vehicle: str

    departure_time: Optional[dt.datetime] = None

    status: Optional[DeliveryTripStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    driver_address: Optional[str] = None

    driver_email: Optional[str] = None

    employee: Optional[str] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    delivery_stops: list[DeliveryStopRead] = []





DeliveryTripListResponse = Page[DeliveryTripRead]

"""Pydantic v2 schemas for Shipment."""





from __future__ import annotations

from app.stock.shipment_domain.models.shipment import (

    ShipmentPickupFromType,

    ShipmentDeliveryToType,

    ShipmentPallets,

    ShipmentShipmentType,

    ShipmentPickupType,

    ShipmentStatus,

    ShipmentTrackingStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.shipment_parcel_domain.schemas.shipment_parcel import (

    ShipmentParcelCreate,

    ShipmentParcelRead,

)

from app.stock.shipment_delivery_note_domain.schemas.shipment_delivery_note import (

    ShipmentDeliveryNoteCreate,

    ShipmentDeliveryNoteRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ShipmentCreate",

    "ShipmentUpdate",

    "ShipmentRead",

    "ShipmentListResponse",

]





class ShipmentBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    pickup_from_type: Optional[ShipmentPickupFromType] = None

    pickup_company: Optional[str] = None

    pickup_customer: Optional[str] = None

    pickup_supplier: Optional[str] = None

    pickup: Optional[str] = None

    pickup_address_name: str

    pickup_address: Optional[str] = None

    pickup_contact_name: Optional[str] = None

    pickup_contact_email: Optional[str] = None

    pickup_contact: Optional[str] = None

    delivery_to_type: Optional[ShipmentDeliveryToType] = None

    delivery_company: Optional[str] = None

    delivery_customer: Optional[str] = None

    delivery_supplier: Optional[str] = None

    delivery_to: Optional[str] = None

    delivery_address_name: str

    delivery_address: Optional[str] = None

    delivery_contact_name: Optional[str] = None

    delivery_contact_email: Optional[str] = None

    delivery_contact: Optional[str] = None

    parcel_template_id: Optional[uuid.UUID] = None

    pallets: Optional[ShipmentPallets] = None

    value_of_goods: Decimal

    pickup_date: dt.date

    pickup_from: dt.time

    pickup_to: dt.time

    shipment_type: Optional[ShipmentShipmentType] = None

    pickup_type: Optional[ShipmentPickupType] = None

    description_of_content: str

    service_provider: Optional[str] = None

    shipment_id: Optional[str] = None

    shipment_amount: Optional[Decimal] = None

    status: Optional[ShipmentStatus] = None

    tracking_url: Optional[str] = None

    carrier: Optional[str] = None

    carrier_service: Optional[str] = None

    awb_number: Optional[str] = None

    tracking_status: Optional[ShipmentTrackingStatus] = None

    tracking_status_info: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    pickup_contact_person: Optional[str] = None

    total_weight: Optional[Decimal] = None

    shipment_parcel: list[ShipmentParcelCreate] = []

    shipment_delivery_note: list[ShipmentDeliveryNoteCreate] = []





class ShipmentCreate(ShipmentBase):

    pass





class ShipmentUpdate(InputSchema):

    """A partial update."""



    pickup_from_type: Optional[ShipmentPickupFromType] = None

    pickup_company: Optional[str] = None

    pickup_customer: Optional[str] = None

    pickup_supplier: Optional[str] = None

    pickup: Optional[str] = None

    pickup_address_name: Optional[str] = None

    pickup_address: Optional[str] = None

    pickup_contact_name: Optional[str] = None

    pickup_contact_email: Optional[str] = None

    pickup_contact: Optional[str] = None

    delivery_to_type: Optional[ShipmentDeliveryToType] = None

    delivery_company: Optional[str] = None

    delivery_customer: Optional[str] = None

    delivery_supplier: Optional[str] = None

    delivery_to: Optional[str] = None

    delivery_address_name: Optional[str] = None

    delivery_address: Optional[str] = None

    delivery_contact_name: Optional[str] = None

    delivery_contact_email: Optional[str] = None

    delivery_contact: Optional[str] = None

    parcel_template_id: Optional[uuid.UUID] = None

    pallets: Optional[ShipmentPallets] = None

    value_of_goods: Optional[Decimal] = None

    pickup_date: Optional[dt.date] = None

    pickup_from: Optional[dt.time] = None

    pickup_to: Optional[dt.time] = None

    shipment_type: Optional[ShipmentShipmentType] = None

    pickup_type: Optional[ShipmentPickupType] = None

    description_of_content: Optional[str] = None

    service_provider: Optional[str] = None

    shipment_id: Optional[str] = None

    shipment_amount: Optional[Decimal] = None

    status: Optional[ShipmentStatus] = None

    tracking_url: Optional[str] = None

    carrier: Optional[str] = None

    carrier_service: Optional[str] = None

    awb_number: Optional[str] = None

    tracking_status: Optional[ShipmentTrackingStatus] = None

    tracking_status_info: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    pickup_contact_person: Optional[str] = None

    total_weight: Optional[Decimal] = None

    shipment_parcel: Optional[list[ShipmentParcelCreate]] = None

    shipment_delivery_note: Optional[list[ShipmentDeliveryNoteCreate]] = None





class ShipmentRead(ReadSchema):

    id: uuid.UUID

    name: str

    pickup_from_type: Optional[ShipmentPickupFromType] = None

    pickup_company: Optional[str] = None

    pickup_customer: Optional[str] = None

    pickup_supplier: Optional[str] = None

    pickup: Optional[str] = None

    pickup_address_name: str

    pickup_address: Optional[str] = None

    pickup_contact_name: Optional[str] = None

    pickup_contact_email: Optional[str] = None

    pickup_contact: Optional[str] = None

    delivery_to_type: Optional[ShipmentDeliveryToType] = None

    delivery_company: Optional[str] = None

    delivery_customer: Optional[str] = None

    delivery_supplier: Optional[str] = None

    delivery_to: Optional[str] = None

    delivery_address_name: str

    delivery_address: Optional[str] = None

    delivery_contact_name: Optional[str] = None

    delivery_contact_email: Optional[str] = None

    delivery_contact: Optional[str] = None

    parcel_template_id: Optional[uuid.UUID] = None

    pallets: Optional[ShipmentPallets] = None

    value_of_goods: Optional[Decimal] = None

    pickup_date: Optional[dt.date] = None

    pickup_from: Optional[dt.time] = None

    pickup_to: Optional[dt.time] = None

    shipment_type: Optional[ShipmentShipmentType] = None

    pickup_type: Optional[ShipmentPickupType] = None

    description_of_content: str

    service_provider: Optional[str] = None

    shipment_id: Optional[str] = None

    shipment_amount: Optional[Decimal] = None

    status: Optional[ShipmentStatus] = None

    tracking_url: Optional[str] = None

    carrier: Optional[str] = None

    carrier_service: Optional[str] = None

    awb_number: Optional[str] = None

    tracking_status: Optional[ShipmentTrackingStatus] = None

    tracking_status_info: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    incoterm: Optional[str] = None

    pickup_contact_person: Optional[str] = None

    total_weight: Optional[Decimal] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    shipment_parcel: list[ShipmentParcelRead] = []

    shipment_delivery_note: list[ShipmentDeliveryNoteRead] = []





ShipmentListResponse = Page[ShipmentRead]

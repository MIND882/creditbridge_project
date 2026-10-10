"""

Shipment -- converted from ``erpnext/stock/doctype/shipment``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.shipment_parcel_domain.models.shipment_parcel import ShipmentParcel

from app.stock.shipment_delivery_note_domain.models.shipment_delivery_note import ShipmentDeliveryNote



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["Shipment", "ShipmentPickupFromType", "ShipmentDeliveryToType", "ShipmentPallets", "ShipmentShipmentType", "ShipmentPickupType", "ShipmentStatus", "ShipmentTrackingStatus"]





class ShipmentPickupFromType(str, enum.Enum):

    COMPANY = "Company"

    CUSTOMER = "Customer"

    SUPPLIER = "Supplier"



class ShipmentDeliveryToType(str, enum.Enum):

    COMPANY = "Company"

    CUSTOMER = "Customer"

    SUPPLIER = "Supplier"



class ShipmentPallets(str, enum.Enum):

    NO = "No"

    YES = "Yes"



class ShipmentShipmentType(str, enum.Enum):

    GOODS = "Goods"

    DOCUMENTS = "Documents"



class ShipmentPickupType(str, enum.Enum):

    PICKUP = "Pickup"

    SELF_DELIVERY = "Self delivery"



class ShipmentStatus(str, enum.Enum):

    DRAFT = "Draft"

    SUBMITTED = "Submitted"

    BOOKED = "Booked"

    CANCELLED = "Cancelled"

    COMPLETED = "Completed"



class ShipmentTrackingStatus(str, enum.Enum):

    IN_PROGRESS = "In Progress"

    DELIVERED = "Delivered"

    RETURNED = "Returned"

    LOST = "Lost"





class Shipment(SubmittableModel, TenantModel):

    __tablename__ = "shipments"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_shipments_business_name"),

    )



    #: ``autoname`` = 'SHIPMENT-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    pickup_from_type: Mapped[Optional[str]] = mapped_column(SAEnum(ShipmentPickupFromType, native_enum=False, length=12, validate_strings=True), nullable=True)

    pickup_company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pickup_customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pickup_supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pickup: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pickup_address_name: Mapped[str] = mapped_column(String(140), nullable=False)

    pickup_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    pickup_contact_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pickup_contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pickup_contact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    delivery_to_type: Mapped[Optional[str]] = mapped_column(SAEnum(ShipmentDeliveryToType, native_enum=False, length=12, validate_strings=True), nullable=True)

    delivery_company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivery_customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivery_supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivery_to: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivery_address_name: Mapped[str] = mapped_column(String(140), nullable=False)

    delivery_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    delivery_contact_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivery_contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivery_contact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    parcel_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipment_parcel_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parcel_template = relationship("ShipmentParcelTemplate", foreign_keys=[parcel_template_id])

    pallets: Mapped[Optional[str]] = mapped_column(SAEnum(ShipmentPallets, native_enum=False, length=7, validate_strings=True), nullable=True)

    value_of_goods: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    pickup_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    pickup_from: Mapped[dt.time] = mapped_column(Time, nullable=False)

    pickup_to: Mapped[dt.time] = mapped_column(Time, nullable=False)

    shipment_type: Mapped[Optional[str]] = mapped_column(SAEnum(ShipmentShipmentType, native_enum=False, length=13, validate_strings=True), nullable=True)

    pickup_type: Mapped[Optional[str]] = mapped_column(SAEnum(ShipmentPickupType, native_enum=False, length=17, validate_strings=True), nullable=True)

    description_of_content: Mapped[str] = mapped_column(String(140), nullable=False)

    service_provider: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipment_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipment_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(ShipmentStatus, native_enum=False, length=13, validate_strings=True), nullable=True)

    tracking_url: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    carrier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    carrier_service: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    awb_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tracking_status: Mapped[Optional[str]] = mapped_column(SAEnum(ShipmentTrackingStatus, native_enum=False, length=15, validate_strings=True), nullable=True)

    tracking_status_info: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipments.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("Shipment", foreign_keys=[amended_from_id])

    incoterm: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pickup_contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    shipment_parcel: Mapped[list["ShipmentParcel"]] = relationship(  # noqa: F821

        "ShipmentParcel",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ShipmentParcel.parent_id]",

    )



    shipment_delivery_note: Mapped[list["ShipmentDeliveryNote"]] = relationship(  # noqa: F821

        "ShipmentDeliveryNote",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ShipmentDeliveryNote.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Shipment id={self.id}>"

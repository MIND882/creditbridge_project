"""

Delivery Trip -- converted from ``erpnext/stock/doctype/delivery_trip``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.delivery_stop_domain.models.delivery_stop import DeliveryStop



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["DeliveryTrip", "DeliveryTripNamingSeries", "DeliveryTripStatus"]





class DeliveryTripNamingSeries(str, enum.Enum):

    MAT_DT_YYYY = "MAT-DT-.YYYY.-"



class DeliveryTripStatus(str, enum.Enum):

    DRAFT = "Draft"

    SCHEDULED = "Scheduled"

    IN_TRANSIT = "In Transit"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"





class DeliveryTrip(SubmittableModel, TenantModel):

    __tablename__ = "delivery_trips"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_delivery_trips_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[Optional[str]] = mapped_column(SAEnum(DeliveryTripNamingSeries, native_enum=False, length=18, validate_strings=True), nullable=True)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    email_notification_sent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    driver: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    driver_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_distance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])

    vehicle: Mapped[str] = mapped_column(String(140), nullable=False)

    departure_time: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(DeliveryTripStatus, native_enum=False, length=14, validate_strings=True), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_trips.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("DeliveryTrip", foreign_keys=[amended_from_id])

    driver_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    driver_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    employee: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    delivery_stops: Mapped[list["DeliveryStop"]] = relationship(  # noqa: F821

        "DeliveryStop",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[DeliveryStop.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<DeliveryTrip id={self.id}>"

"""

Delivery Stop -- converted from ``erpnext/stock/doctype/delivery_stop``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Delivery Trip).

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["DeliveryStop"]







class DeliveryStop(ChildTableModel, TenantModel):

    __tablename__ = "delivery_stops"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_delivery_stops_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_trips.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "DeliveryTrip",

        back_populates="delivery_stops",

        # explicit: a child can carry a second FK to its own parent

        # (item_variant_attribute.variant_of -> items), which would

        # otherwise make the join ambiguous

        foreign_keys=[parent_id],

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address: Mapped[str] = mapped_column(String(140), nullable=False)

    locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    customer_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    visited: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    delivery_note_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_notes.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    delivery_note = relationship("DeliveryNote", foreign_keys=[delivery_note_id])

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    contact: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    email_sent_to: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_contact: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    distance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    estimated_arrival: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    lat: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])

    lng: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<DeliveryStop id={self.id}>"

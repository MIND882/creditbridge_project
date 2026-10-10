"""

Shipment Delivery Note -- converted from ``erpnext/stock/doctype/shipment_delivery_note``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Shipment).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ShipmentDeliveryNote"]







class ShipmentDeliveryNote(ChildTableModel, TenantModel):

    __tablename__ = "shipment_delivery_notes"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_shipment_delivery_notes_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipments.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "Shipment",

        back_populates="shipment_delivery_note",

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



    delivery_note_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_notes.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    delivery_note = relationship("DeliveryNote", foreign_keys=[delivery_note_id])

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ShipmentDeliveryNote id={self.id}>"

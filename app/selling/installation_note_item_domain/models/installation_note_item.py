"""

Installation Note Item -- converted from ``erpnext/selling/doctype/installation_note_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Installation Note).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["InstallationNoteItem"]







class InstallationNoteItem(ChildTableModel, TenantModel):

    __tablename__ = "installation_note_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_installation_note_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("installation_notes.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.selling.installation_note_domain.models.installation_note.InstallationNote",

        back_populates="items",

        # explicit: a child can carry a second FK to its own parent

        # (item_variant_attribute.variant_of -> items), which would

        # otherwise make the join ambiguous

        foreign_keys=[parent_id],

    )

    parenttype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    parentfield: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_code_id])

    serial_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    prevdoc_detail_docname: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    prevdoc_docname: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    prevdoc_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    serial_and_batch_bundle = relationship("app.stock.serial_and_batch_bundle_domain.models.serial_and_batch_bundle.SerialAndBatchBundle", foreign_keys=[serial_and_batch_bundle_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<InstallationNoteItem id={self.id}>"

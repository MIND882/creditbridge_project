"""

Packed Item -- converted from ``erpnext/stock/doctype/packed_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Delivery Note).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PackedItem"]







class PackedItem(ChildTableModel, TenantModel):

    __tablename__ = "packed_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_packed_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_notes.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "DeliveryNote",

        back_populates="packed_items",

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



    parent_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parent_item = relationship("Item", foreign_keys=[parent_item_id])

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    product_bundle: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    target_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    target_warehouse = relationship("Warehouse", foreign_keys=[target_warehouse_id])

    qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batchs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    projected_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])

    page_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    prevdoc_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    parent_detail_docname: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    actual_batch_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    incoming_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    conversion_factor: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ordered_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    picked_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    packed_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    serial_and_batch_bundle = relationship("SerialAndBatchBundle", foreign_keys=[serial_and_batch_bundle_id])

    use_serial_batch_fields: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    delivered_by_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    requested_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    reserve_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PackedItem id={self.id}>"

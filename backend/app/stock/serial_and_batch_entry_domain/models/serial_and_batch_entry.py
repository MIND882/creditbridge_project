"""

Serial and Batch Entry -- converted from ``erpnext/stock/doctype/serial_and_batch_entry``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Serial And Batch Bundle).

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SerialAndBatchEntry"]







class SerialAndBatchEntry(ChildTableModel, TenantModel):

    __tablename__ = "serial_and_batch_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_serial_and_batch_entrys_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "SerialAndBatchBundle",

        back_populates="entries",

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



    serial_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_nos.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    serial_no = relationship("SerialNo", foreign_keys=[serial_no_id])

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batches.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])

    qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=1)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    incoming_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    outgoing_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_value_difference: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    is_outward: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    stock_queue: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivered_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    reference_for_reservation: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_datetime: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_detail_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    type_of_transaction: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_cancelled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SerialAndBatchEntry id={self.id}>"

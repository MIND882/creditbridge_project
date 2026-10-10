"""

Stock Reconciliation Item -- converted from ``erpnext/stock/doctype/stock_reconciliation_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Stock Reconciliation).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["StockReconciliationItem"]







class StockReconciliationItem(ChildTableModel, TenantModel):

    __tablename__ = "stock_reconciliation_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_stock_reconciliation_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_reconciliations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "StockReconciliation",

        back_populates="items",

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



    barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    valuation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    current_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    current_serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    current_valuation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    current_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    quantity_difference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amount_difference: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batches.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])

    allow_zero_valuation_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    has_item_scanned: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    serial_and_batch_bundle = relationship("SerialAndBatchBundle", foreign_keys=[serial_and_batch_bundle_id])

    current_serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    current_serial_and_batch_bundle = relationship("SerialAndBatchBundle", foreign_keys=[current_serial_and_batch_bundle_id])

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("ItemGroup", foreign_keys=[item_group_id])

    use_serial_batch_fields: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    reconcile_all_serial_batch: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockReconciliationItem id={self.id}>"

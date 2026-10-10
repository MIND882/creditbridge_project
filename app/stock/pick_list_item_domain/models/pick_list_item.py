"""

Pick List Item -- converted from ``erpnext/stock/doctype/pick_list_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Pick List).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PickListItem"]







class PickListItem(ChildTableModel, TenantModel):

    __tablename__ = "pick_list_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_pick_list_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pick_lists.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "PickList",

        back_populates="locations",

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



    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=1)

    picked_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    serial_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batchs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])

    conversion_factor: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    sales_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    material_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    material_request = relationship("MaterialRequest", foreign_keys=[material_request_id])

    material_request_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    product_bundle_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    serial_and_batch_bundle = relationship("SerialAndBatchBundle", foreign_keys=[serial_and_batch_bundle_id])

    stock_reserved_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    use_serial_batch_fields: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    delivered_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    transferred_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    company_total_stock: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PickListItem id={self.id}>"

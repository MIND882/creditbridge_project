"""

Work Order Item -- converted from ``erpnext/manufacturing/doctype/work_order_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Work Order).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["WorkOrderItem"]







class WorkOrderItem(ChildTableModel, TenantModel):

    __tablename__ = "work_order_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_work_order_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("work_orders.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.work_order_domain.models.work_order.WorkOrder",

        back_populates="required_items",

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



    operation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("operations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    operation = relationship("app.manufacturing.operation_domain.models.operation.Operation", foreign_keys=[operation_id])

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_code_id])

    source_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    source_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[source_warehouse_id])

    operation_row_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    allow_alternative_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    include_item_in_manufacturing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    required_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    transferred_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    consumed_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    returned_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    available_qty_at_source_warehouse: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    available_qty_at_wip_warehouse: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_reserved_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    is_additional_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_customer_provided_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    voucher_detail_reference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<WorkOrderItem id={self.id}>"

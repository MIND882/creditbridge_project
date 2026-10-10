"""

BOM Item -- converted from ``erpnext/manufacturing/doctype/bom_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Bom).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BomItem"]







class BomItem(ChildTableModel, TenantModel):

    __tablename__ = "bom_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bom_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.bom_domain.models.bom.Bom",

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

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    operation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("operations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    operation = relationship("app.manufacturing.operation_domain.models.operation.Operation", foreign_keys=[operation_id])

    operation_row_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    do_not_explode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    bom_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bom_no = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[bom_no_id])

    source_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    source_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[source_warehouse_id])

    allow_alternative_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_stock_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    image_view: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    conversion_factor: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    base_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    qty_consumed_per_unit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    has_variants: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    include_item_in_manufacturing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    original_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    original_item = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[original_item_id])

    sourced_by_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_sub_assembly_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_phantom_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BomItem id={self.id}>"

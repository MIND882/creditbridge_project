"""

Item Reorder -- converted from ``erpnext/stock/doctype/item_reorder``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Item).

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ItemReorder", "ItemReorderMaterialRequestType"]





class ItemReorderMaterialRequestType(str, enum.Enum):

    PURCHASE = "Purchase"

    TRANSFER = "Transfer"

    MATERIAL_ISSUE = "Material Issue"

    MANUFACTURE = "Manufacture"





class ItemReorder(ChildTableModel, TenantModel):

    __tablename__ = "item_reorders"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_reorders_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "Item",

        back_populates="reorder_levels",

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



    warehouse_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse_group = relationship("Warehouse", foreign_keys=[warehouse_group_id])

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    warehouse_reorder_level: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    warehouse_reorder_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    material_request_type: Mapped[str] = mapped_column(SAEnum(ItemReorderMaterialRequestType, native_enum=False, length=18, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemReorder id={self.id}>"

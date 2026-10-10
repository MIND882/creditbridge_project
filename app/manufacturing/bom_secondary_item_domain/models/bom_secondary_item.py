"""

BOM Secondary Item -- converted from ``erpnext/manufacturing/doctype/bom_secondary_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Bom).

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BomSecondaryItem", "BomSecondaryItemSecondaryItemType"]





class BomSecondaryItemSecondaryItemType(str, enum.Enum):

    CO_PRODUCT = "Co-Product"

    BY_PRODUCT = "By-Product"

    SCRAP = "Scrap"

    ADDITIONAL_FINISHED_GOOD = "Additional Finished Good"





class BomSecondaryItem(ChildTableModel, TenantModel):

    __tablename__ = "bom_secondary_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bom_secondary_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.bom_domain.models.bom.Bom",

        back_populates="secondary_items",

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



    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    is_legacy: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_code_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    secondary_item_type: Mapped[Optional[str]] = mapped_column(SAEnum(BomSecondaryItemSecondaryItemType, native_enum=False, length=28, validate_strings=True), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=1)

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image_nygv: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    cost_allocation_per: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    process_loss_per: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    cost: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    base_cost: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    process_loss_qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BomSecondaryItem id={self.id}>"

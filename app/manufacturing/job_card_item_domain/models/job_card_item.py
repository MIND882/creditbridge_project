"""

Job Card Item -- converted from ``erpnext/manufacturing/doctype/job_card_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Job Card).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["JobCardItem"]







class JobCardItem(ChildTableModel, TenantModel):

    __tablename__ = "job_card_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_job_card_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("job_cards.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.job_card_domain.models.job_card.JobCard",

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

    source_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    source_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[source_warehouse_id])

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("app.stock.item_group_domain.models.item_group.ItemGroup", foreign_keys=[item_group_id])

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    required_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    transferred_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    consumed_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    allow_alternative_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<JobCardItem id={self.id}>"

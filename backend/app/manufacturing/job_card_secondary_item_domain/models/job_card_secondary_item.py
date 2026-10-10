"""

Job Card Secondary Item -- converted from ``erpnext/manufacturing/doctype/job_card_secondary_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Job Card).

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



__all__ = ["JobCardSecondaryItem", "JobCardSecondaryItemSecondaryItemType"]





class JobCardSecondaryItemSecondaryItemType(str, enum.Enum):

    CO_PRODUCT = "Co-Product"

    BY_PRODUCT = "By-Product"

    SCRAP = "Scrap"

    ADDITIONAL_FINISHED_GOOD = "Additional Finished Good"





class JobCardSecondaryItem(ChildTableModel, TenantModel):

    __tablename__ = "job_card_secondary_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_job_card_secondary_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("job_cards.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.job_card_domain.models.job_card.JobCard",

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



    secondary_item_type: Mapped[str] = mapped_column(SAEnum(JobCardSecondaryItemSecondaryItemType, native_enum=False, length=28, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_code_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bom_secondary_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    stock_qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<JobCardSecondaryItem id={self.id}>"

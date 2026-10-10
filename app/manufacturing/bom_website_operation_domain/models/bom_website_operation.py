"""

BOM Website Operation -- converted from ``erpnext/manufacturing/doctype/bom_website_operation``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Bom).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BomWebsiteOperation"]







class BomWebsiteOperation(ChildTableModel, TenantModel):

    __tablename__ = "bom_website_operations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bom_website_operations_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.bom_domain.models.bom.Bom",

        back_populates="website_operations",

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

        nullable=False, index=True,

    )

    operation = relationship("app.manufacturing.operation_domain.models.operation.Operation", foreign_keys=[operation_id])

    workstation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    workstation = relationship("app.manufacturing.workstation_domain.models.workstation.Workstation", foreign_keys=[workstation_id])

    time_in_mins: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    website_image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    thumbnail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BomWebsiteOperation id={self.id}>"

"""

Workstation Cost -- converted from ``erpnext/manufacturing/doctype/workstation_cost``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Workstation).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["WorkstationCost"]







class WorkstationCost(ChildTableModel, TenantModel):

    __tablename__ = "workstation_costs"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_workstation_costs_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.workstation_domain.models.workstation.Workstation",

        back_populates="workstation_costs",

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



    operating_component_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstation_operating_components.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    operating_component = relationship("app.manufacturing.workstation_operating_component_domain.models.workstation_operating_component.WorkstationOperatingComponent", foreign_keys=[operating_component_id])

    operating_cost: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<WorkstationCost id={self.id}>"

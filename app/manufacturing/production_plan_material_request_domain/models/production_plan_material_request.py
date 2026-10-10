"""

Production Plan Material Request -- converted from ``erpnext/manufacturing/doctype/production_plan_material_request``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Master Production Schedule).

"""



from __future__ import annotations



import datetime as dt

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ProductionPlanMaterialRequest"]







class ProductionPlanMaterialRequest(ChildTableModel, TenantModel):

    __tablename__ = "production_plan_material_requests"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_production_plan_material_requests_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("master_production_schedules.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.master_production_schedule_domain.models.master_production_schedule.MasterProductionSchedule",

        back_populates="material_requests",

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



    material_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    material_request = relationship("app.stock.material_request_domain.models.material_request.MaterialRequest", foreign_keys=[material_request_id])

    material_request_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProductionPlanMaterialRequest id={self.id}>"

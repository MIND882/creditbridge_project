"""

Cost Center Allocation -- converted from

``erpnext/accounts/doctype/cost_center_allocation``.



Submittable (``is_submittable: 1``), so it carries ``docstatus`` and the

submit / cancel / amend lifecycle. ``company`` collapses into ``business_id``.



``autoname`` is ``CC-ALLOC-.#####`` -- a per-tenant counter, implemented by the

service rather than the database so the sequence cannot leak across tenants.

"""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional



from sqlalchemy import Date, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index

from app.core.docstatus import SubmittableModel



__all__ = ["CostCenterAllocation"]





class CostCenterAllocation(SubmittableModel, TenantModel):

    """

    Splits one main cost centre's postings across several others, from a date.



    ``allocation_percentages`` must total exactly 100 -- enforced by the

    service, per ``validate_total_allocation_percentage``.

    """



    __tablename__ = "cost_center_allocations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_cc_alloc_business_id_name"),

        tenant_index("ix_cc_alloc_business_main", "main_cost_center_id"),

        tenant_index("ix_cc_alloc_business_valid_from", "valid_from"),

    )



    #: e.g. ``CC-ALLOC-00001``. Scoped per tenant.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    main_cost_center_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"), nullable=False

    )

    main_cost_center = relationship("CostCenter", foreign_keys=[main_cost_center_id])



    valid_from: Mapped[date] = mapped_column(Date, nullable=False)



    #: ERPNext's ``amended_from`` Link: the cancelled record this one replaces.

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_center_allocations.id", ondelete="SET NULL"), nullable=True

    )



    allocation_percentages: Mapped[list["CostCenterAllocationPercentage"]] = relationship(  # noqa: F821

        "CostCenterAllocationPercentage",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="CostCenterAllocationPercentage.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CostCenterAllocation id={self.id} name={self.name!r}>"

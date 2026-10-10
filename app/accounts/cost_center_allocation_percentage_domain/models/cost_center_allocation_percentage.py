"""

Cost Center Allocation Percentage -- converted from

``erpnext/accounts/doctype/cost_center_allocation_percentage``.



A Frappe child table (``istable: 1``): no independent identity, owned by a Cost

Center Allocation, ordered by ``idx``, never addressed by its own API.



Fields:

    cost_center   Link Cost Center  required

    percentage    Percent           required

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import TYPE_CHECKING, Optional



from sqlalchemy import ForeignKey, Numeric

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



if TYPE_CHECKING:  # pragma: no cover

    from app.accounts.cost_center_allocation_domain.models.cost_center_allocation import (

        CostCenterAllocation,

    )



__all__ = ["CostCenterAllocationPercentage"]





class CostCenterAllocationPercentage(ChildTableModel, TenantModel):

    """One row of an allocation split: this cost centre takes this percentage."""



    __tablename__ = "cost_center_allocation_percentages"



    #: Re-declared from the mixin with a concrete FK, so the constraint is real

    #: rather than a bare UUID column.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_center_allocations.id", ondelete="CASCADE"),

        nullable=True,

        index=True,

    )

    parent: Mapped[Optional["CostCenterAllocation"]] = relationship(

        "CostCenterAllocation", back_populates="allocation_percentages"

    )



    cost_center_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])



    #: ERPNext `Percent` -> exact decimal. A float percentage cannot sum to

    #: exactly 100 reliably, and the service compares against exactly 100.

    percentage: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CostCenterAllocationPercentage id={self.id} pct={self.percentage}>"

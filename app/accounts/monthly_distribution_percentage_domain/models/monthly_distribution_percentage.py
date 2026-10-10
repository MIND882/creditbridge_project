"""

Monthly Distribution Percentage -- converted from ``erpnext/accounts/doctype/monthly_distribution_percentage``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["MonthlyDistributionPercentage"]







class MonthlyDistributionPercentage(ChildTableModel, TenantModel):

    __tablename__ = "monthly_distribution_percentages"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_monthly_distribution_percentages_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("monthly_distributions.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("MonthlyDistribution", back_populates="percentages", foreign_keys=[parent_id])



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    month: Mapped[str] = mapped_column(String(140), nullable=False)

    percentage_allocation: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<MonthlyDistributionPercentage id={self.id}>"

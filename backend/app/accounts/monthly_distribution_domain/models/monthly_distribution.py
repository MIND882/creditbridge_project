"""

Monthly Distribution -- converted from ``erpnext/accounts/doctype/monthly_distribution``.





"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.monthly_distribution_percentage_domain.models.monthly_distribution_percentage import MonthlyDistributionPercentage



from app.accounts.fiscal_year_domain.models.fiscal_year import FiscalYear  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["MonthlyDistribution"]







class MonthlyDistribution(TenantModel):

    __tablename__ = "monthly_distributions"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_monthly_distributions_business_name"),

    )



    #: ``autoname`` = 'field:distribution_id'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    distribution_id: Mapped[str] = mapped_column(String(140), nullable=False)

    fiscal_year_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("fiscal_years.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    fiscal_year = relationship("FiscalYear", foreign_keys=[fiscal_year_id])



    percentages = relationship(

        MonthlyDistributionPercentage,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=MonthlyDistributionPercentage.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<MonthlyDistribution id={self.id}>"

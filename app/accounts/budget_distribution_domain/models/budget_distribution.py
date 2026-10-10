"""

Budget Distribution -- converted from ``erpnext/accounts/doctype/budget_distribution``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BudgetDistribution"]







class BudgetDistribution(ChildTableModel, TenantModel):

    __tablename__ = "budget_distributions"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("budgets.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("Budget", back_populates="budget_distribution", foreign_keys=[parent_id])



    start_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    end_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    percent: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BudgetDistribution id={self.id}>"

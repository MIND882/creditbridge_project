"""

Supplier Scorecard Criteria -- converted from ``erpnext/buying/doctype/supplier_scorecard_criteria``.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["SupplierScorecardCriteria"]







class SupplierScorecardCriteria(TenantModel):

    __tablename__ = "supplier_scorecard_criterias"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_supplier_scorecard_criterias_business_name"),

    )



    #: ``autoname`` = 'field:criteria_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    criteria_name: Mapped[str] = mapped_column(String(140), nullable=False)

    max_score: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=100)

    formula: Mapped[str] = mapped_column(String(140), nullable=False)

    weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierScorecardCriteria id={self.id}>"

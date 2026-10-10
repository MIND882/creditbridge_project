"""

Supplier Scorecard Variable -- converted from ``erpnext/buying/doctype/supplier_scorecard_variable``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["SupplierScorecardVariable"]







class SupplierScorecardVariable(TenantModel):

    __tablename__ = "supplier_scorecard_variables"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_supplier_scorecard_variables_business_name"),

    )



    #: ``autoname`` = 'field:variable_label' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    variable_label: Mapped[str] = mapped_column(String(140), nullable=False)

    is_custom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    param_name: Mapped[str] = mapped_column(String(140), nullable=False)

    path: Mapped[str] = mapped_column(String(140), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierScorecardVariable id={self.id}>"

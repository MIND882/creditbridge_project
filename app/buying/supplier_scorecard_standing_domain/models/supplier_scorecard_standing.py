"""

Supplier Scorecard Standing -- converted from ``erpnext/buying/doctype/supplier_scorecard_standing``.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["SupplierScorecardStanding", "SupplierScorecardStandingStandingColor"]





class SupplierScorecardStandingStandingColor(str, enum.Enum):

    BLUE = "Blue"

    PURPLE = "Purple"

    GREEN = "Green"

    YELLOW = "Yellow"

    ORANGE = "Orange"

    RED = "Red"





class SupplierScorecardStanding(TenantModel):

    __tablename__ = "supplier_scorecard_standings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_supplier_scorecard_standings_business_name"),

    )



    #: ``autoname`` = 'field:standing_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    standing_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    standing_color: Mapped[Optional[str]] = mapped_column(SAEnum(SupplierScorecardStandingStandingColor, native_enum=False, length=10, validate_strings=True), nullable=True)

    min_grade: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_grade: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    warn_rfqs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    warn_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    prevent_rfqs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    prevent_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    notify_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    notify_employee: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    employee_link: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierScorecardStanding id={self.id}>"

"""

Supplier Scorecard -- converted from ``erpnext/buying/doctype/supplier_scorecard``.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.buying.supplier_scorecard_scoring_standing_domain.models.supplier_scorecard_scoring_standing import SupplierScorecardScoringStanding

from app.buying.supplier_scorecard_scoring_criteria_domain.models.supplier_scorecard_scoring_criteria import SupplierScorecardScoringCriteria



from app.core.base_model import TenantModel



__all__ = ["SupplierScorecard", "SupplierScorecardPeriod"]





class SupplierScorecardPeriod(str, enum.Enum):

    PER_WEEK = "Per Week"

    PER_MONTH = "Per Month"

    PER_YEAR = "Per Year"





class SupplierScorecard(TenantModel):

    __tablename__ = "supplier_scorecards"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_supplier_scorecards_business_name"),

    )



    #: ``autoname`` = 'field:supplier' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    supplier_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("suppliers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    supplier = relationship("app.buying.supplier_domain.models.supplier.Supplier", foreign_keys=[supplier_id])

    supplier_score: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    indicator_color: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    period: Mapped[str] = mapped_column(SAEnum(SupplierScorecardPeriod, native_enum=False, length=13, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    weighting_function: Mapped[str] = mapped_column(String(140), nullable=False)

    warn_rfqs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    warn_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    prevent_rfqs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    prevent_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    notify_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    notify_employee: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    employee: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    standings: Mapped[list["SupplierScorecardScoringStanding"]] = relationship(  # noqa: F821

        "SupplierScorecardScoringStanding",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[SupplierScorecardScoringStanding.parent_id]",

    )



    criteria: Mapped[list["SupplierScorecardScoringCriteria"]] = relationship(  # noqa: F821

        "SupplierScorecardScoringCriteria",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[SupplierScorecardScoringCriteria.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierScorecard id={self.id}>"

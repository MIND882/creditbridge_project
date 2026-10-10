"""

Supplier Scorecard Period -- converted from ``erpnext/buying/doctype/supplier_scorecard_period``.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.buying.supplier_scorecard_scoring_variable_domain.models.supplier_scorecard_scoring_variable import SupplierScorecardScoringVariable



from app.core.base_model import TenantModel



__all__ = ["SupplierScorecardPeriod", "SupplierScorecardPeriodNamingSeries"]





class SupplierScorecardPeriodNamingSeries(str, enum.Enum):

    PU_SSP_YYYY = "PU-SSP-.YYYY.-"





class SupplierScorecardPeriod(TenantModel):

    __tablename__ = "supplier_scorecard_periods"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_supplier_scorecard_periods_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    supplier_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("suppliers.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    supplier = relationship("app.buying.supplier_domain.models.supplier.Supplier", foreign_keys=[supplier_id])

    naming_series: Mapped[str] = mapped_column(SAEnum(SupplierScorecardPeriodNamingSeries, native_enum=False, length=18, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    total_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    start_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    end_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    scorecard_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_scorecards.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    scorecard = relationship("app.buying.supplier_scorecard_domain.models.supplier_scorecard.SupplierScorecard", foreign_keys=[scorecard_id])

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_scorecard_periods.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.buying.supplier_scorecard_period_domain.models.supplier_scorecard_period.SupplierScorecardPeriod", foreign_keys=[amended_from_id])



    variables: Mapped[list["SupplierScorecardScoringVariable"]] = relationship(  # noqa: F821

        "SupplierScorecardScoringVariable",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[SupplierScorecardScoringVariable.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierScorecardPeriod id={self.id}>"

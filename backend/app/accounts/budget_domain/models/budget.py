"""

Budget -- converted from ``erpnext/accounts/doctype/budget``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.budget_distribution_domain.models.budget_distribution import BudgetDistribution



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401

from app.accounts.fiscal_year_domain.models.fiscal_year import FiscalYear  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["Budget", "BudgetBudgetAgainst", "BudgetActionIfAnnualBudgetExceededOnMr", "BudgetActionIfAccumulatedMonthlyBudgetExceededOnMr", "BudgetActionIfAnnualBudgetExceededOnPo", "BudgetActionIfAccumulatedMonthlyBudgetExceededOnPo", "BudgetActionIfAnnualBudgetExceeded", "BudgetActionIfAccumulatedMonthlyBudgetExceeded", "BudgetNamingSeries", "BudgetActionIfAnnualExceededOnCumulativeExpense", "BudgetActionIfAccumulatedMonthlyExceededOnCumulativeExpense", "BudgetDistributionFrequency"]







class BudgetBudgetAgainst(str, enum.Enum):

    COST_CENTER = "Cost Center"

    PROJECT = "Project"





class BudgetActionIfAnnualBudgetExceededOnMr(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"

    IGNORE = "Ignore"





class BudgetActionIfAccumulatedMonthlyBudgetExceededOnMr(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"

    IGNORE = "Ignore"





class BudgetActionIfAnnualBudgetExceededOnPo(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"

    IGNORE = "Ignore"





class BudgetActionIfAccumulatedMonthlyBudgetExceededOnPo(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"

    IGNORE = "Ignore"





class BudgetActionIfAnnualBudgetExceeded(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"

    IGNORE = "Ignore"





class BudgetActionIfAccumulatedMonthlyBudgetExceeded(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"

    IGNORE = "Ignore"





class BudgetNamingSeries(str, enum.Enum):

    BUDGET = "BUDGET-.########"





class BudgetActionIfAnnualExceededOnCumulativeExpense(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"

    IGNORE = "Ignore"





class BudgetActionIfAccumulatedMonthlyExceededOnCumulativeExpense(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"

    IGNORE = "Ignore"





class BudgetDistributionFrequency(str, enum.Enum):

    MONTHLY = "Monthly"

    QUARTERLY = "Quarterly"

    HALF_YEARLY = "Half-Yearly"

    YEARLY = "Yearly"









class Budget(SubmittableModel, TenantModel):

    __tablename__ = "budgets"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_budgets_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    budget_against: Mapped[BudgetBudgetAgainst] = mapped_column(

        SAEnum(BudgetBudgetAgainst, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    applicable_on_material_request: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    action_if_annual_budget_exceeded_on_mr: Mapped[Optional[BudgetActionIfAnnualBudgetExceededOnMr]] = mapped_column(

        SAEnum(BudgetActionIfAnnualBudgetExceededOnMr, native_enum=False, length=6, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    action_if_accumulated_monthly_budget_exceeded_on_mr: Mapped[Optional[BudgetActionIfAccumulatedMonthlyBudgetExceededOnMr]] = mapped_column(

        SAEnum(BudgetActionIfAccumulatedMonthlyBudgetExceededOnMr, native_enum=False, length=6, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    applicable_on_purchase_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    action_if_annual_budget_exceeded_on_po: Mapped[Optional[BudgetActionIfAnnualBudgetExceededOnPo]] = mapped_column(

        SAEnum(BudgetActionIfAnnualBudgetExceededOnPo, native_enum=False, length=6, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    action_if_accumulated_monthly_budget_exceeded_on_po: Mapped[Optional[BudgetActionIfAccumulatedMonthlyBudgetExceededOnPo]] = mapped_column(

        SAEnum(BudgetActionIfAccumulatedMonthlyBudgetExceededOnPo, native_enum=False, length=6, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    applicable_on_booking_actual_expenses: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    action_if_annual_budget_exceeded: Mapped[Optional[BudgetActionIfAnnualBudgetExceeded]] = mapped_column(

        SAEnum(BudgetActionIfAnnualBudgetExceeded, native_enum=False, length=6, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    action_if_accumulated_monthly_budget_exceeded: Mapped[Optional[BudgetActionIfAccumulatedMonthlyBudgetExceeded]] = mapped_column(

        SAEnum(BudgetActionIfAccumulatedMonthlyBudgetExceeded, native_enum=False, length=6, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    naming_series: Mapped[BudgetNamingSeries] = mapped_column(

        SAEnum(BudgetNamingSeries, native_enum=False, length=16, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    applicable_on_cumulative_expense: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    action_if_annual_exceeded_on_cumulative_expense: Mapped[Optional[BudgetActionIfAnnualExceededOnCumulativeExpense]] = mapped_column(

        SAEnum(BudgetActionIfAnnualExceededOnCumulativeExpense, native_enum=False, length=6, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    action_if_accumulated_monthly_exceeded_on_cumulative_expense: Mapped[Optional[BudgetActionIfAccumulatedMonthlyExceededOnCumulativeExpense]] = mapped_column(

        SAEnum(BudgetActionIfAccumulatedMonthlyExceededOnCumulativeExpense, native_enum=False, length=6, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])

    budget_amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    revision_of: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    distribute_equally: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    from_fiscal_year_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("fiscal_years.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    from_fiscal_year = relationship("FiscalYear", foreign_keys=[from_fiscal_year_id])

    to_fiscal_year_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("fiscal_years.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    to_fiscal_year = relationship("FiscalYear", foreign_keys=[to_fiscal_year_id])

    budget_start_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    budget_end_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    distribution_frequency: Mapped[BudgetDistributionFrequency] = mapped_column(

        SAEnum(BudgetDistributionFrequency, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    budget_distribution_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    budget_distribution = relationship(

        BudgetDistribution,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=BudgetDistribution.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Budget id={self.id}>"

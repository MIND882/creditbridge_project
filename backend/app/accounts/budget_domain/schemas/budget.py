"""Pydantic v2 schemas for Budget."""





from __future__ import annotations

from app.accounts.budget_domain.models.budget import (

    BudgetActionIfAccumulatedMonthlyBudgetExceeded,

    BudgetActionIfAccumulatedMonthlyBudgetExceededOnMr,

    BudgetActionIfAccumulatedMonthlyBudgetExceededOnPo,

    BudgetActionIfAccumulatedMonthlyExceededOnCumulativeExpense,

    BudgetActionIfAnnualBudgetExceeded,

    BudgetActionIfAnnualBudgetExceededOnMr,

    BudgetActionIfAnnualBudgetExceededOnPo,

    BudgetActionIfAnnualExceededOnCumulativeExpense,

    BudgetBudgetAgainst,

    BudgetDistributionFrequency,

    BudgetNamingSeries,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.budget_distribution_domain.schemas.budget_distribution import (

    BudgetDistributionCreate,

    BudgetDistributionRead,

)



__all__ = [

    "BudgetCreate",

    "BudgetUpdate",

    "BudgetRead",

    "BudgetListResponse",

]





class BudgetBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    budget_against: BudgetBudgetAgainst = BudgetBudgetAgainst.COST_CENTER

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    amended_from: Optional[str] = None

    applicable_on_material_request: bool = False

    action_if_annual_budget_exceeded_on_mr: Optional[BudgetActionIfAnnualBudgetExceededOnMr] = None

    action_if_accumulated_monthly_budget_exceeded_on_mr: Optional[BudgetActionIfAccumulatedMonthlyBudgetExceededOnMr] = None

    applicable_on_purchase_order: bool = False

    action_if_annual_budget_exceeded_on_po: Optional[BudgetActionIfAnnualBudgetExceededOnPo] = None

    action_if_accumulated_monthly_budget_exceeded_on_po: Optional[BudgetActionIfAccumulatedMonthlyBudgetExceededOnPo] = None

    applicable_on_booking_actual_expenses: bool = False

    action_if_annual_budget_exceeded: Optional[BudgetActionIfAnnualBudgetExceeded] = None

    action_if_accumulated_monthly_budget_exceeded: Optional[BudgetActionIfAccumulatedMonthlyBudgetExceeded] = None

    naming_series: BudgetNamingSeries = BudgetNamingSeries.BUDGET

    applicable_on_cumulative_expense: bool = False

    action_if_annual_exceeded_on_cumulative_expense: Optional[BudgetActionIfAnnualExceededOnCumulativeExpense] = None

    action_if_accumulated_monthly_exceeded_on_cumulative_expense: Optional[BudgetActionIfAccumulatedMonthlyExceededOnCumulativeExpense] = None

    account_id: uuid.UUID

    budget_amount: Optional[Decimal] = None

    revision_of: Optional[str] = None

    distribute_equally: bool = True

    from_fiscal_year_id: uuid.UUID

    to_fiscal_year_id: uuid.UUID

    budget_start_date: Optional[dt.date] = None

    budget_end_date: Optional[dt.date] = None

    distribution_frequency: BudgetDistributionFrequency = BudgetDistributionFrequency.MONTHLY

    budget_distribution_total: Optional[Decimal] = None



    budget_distribution: list[BudgetDistributionCreate] = []





class BudgetCreate(BudgetBase):

    pass





class BudgetUpdate(InputSchema):

    """A partial update."""



    budget_against: Optional[BudgetBudgetAgainst] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    amended_from: Optional[str] = None

    applicable_on_material_request: Optional[bool] = None

    action_if_annual_budget_exceeded_on_mr: Optional[BudgetActionIfAnnualBudgetExceededOnMr] = None

    action_if_accumulated_monthly_budget_exceeded_on_mr: Optional[BudgetActionIfAccumulatedMonthlyBudgetExceededOnMr] = None

    applicable_on_purchase_order: Optional[bool] = None

    action_if_annual_budget_exceeded_on_po: Optional[BudgetActionIfAnnualBudgetExceededOnPo] = None

    action_if_accumulated_monthly_budget_exceeded_on_po: Optional[BudgetActionIfAccumulatedMonthlyBudgetExceededOnPo] = None

    applicable_on_booking_actual_expenses: Optional[bool] = None

    action_if_annual_budget_exceeded: Optional[BudgetActionIfAnnualBudgetExceeded] = None

    action_if_accumulated_monthly_budget_exceeded: Optional[BudgetActionIfAccumulatedMonthlyBudgetExceeded] = None

    naming_series: Optional[BudgetNamingSeries] = None

    applicable_on_cumulative_expense: Optional[bool] = None

    action_if_annual_exceeded_on_cumulative_expense: Optional[BudgetActionIfAnnualExceededOnCumulativeExpense] = None

    action_if_accumulated_monthly_exceeded_on_cumulative_expense: Optional[BudgetActionIfAccumulatedMonthlyExceededOnCumulativeExpense] = None

    account_id: Optional[uuid.UUID] = None

    budget_amount: Optional[Decimal] = None

    revision_of: Optional[str] = None

    distribute_equally: Optional[bool] = None

    from_fiscal_year_id: Optional[uuid.UUID] = None

    to_fiscal_year_id: Optional[uuid.UUID] = None

    budget_start_date: Optional[dt.date] = None

    budget_end_date: Optional[dt.date] = None

    distribution_frequency: Optional[BudgetDistributionFrequency] = None

    budget_distribution_total: Optional[Decimal] = None

    budget_distribution: Optional[list[BudgetDistributionCreate]] = None





class BudgetRead(ReadSchema):

    id: uuid.UUID

    name: str

    budget_against: BudgetBudgetAgainst

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    amended_from: Optional[str] = None

    applicable_on_material_request: bool

    action_if_annual_budget_exceeded_on_mr: Optional[BudgetActionIfAnnualBudgetExceededOnMr] = None

    action_if_accumulated_monthly_budget_exceeded_on_mr: Optional[BudgetActionIfAccumulatedMonthlyBudgetExceededOnMr] = None

    applicable_on_purchase_order: bool

    action_if_annual_budget_exceeded_on_po: Optional[BudgetActionIfAnnualBudgetExceededOnPo] = None

    action_if_accumulated_monthly_budget_exceeded_on_po: Optional[BudgetActionIfAccumulatedMonthlyBudgetExceededOnPo] = None

    applicable_on_booking_actual_expenses: bool

    action_if_annual_budget_exceeded: Optional[BudgetActionIfAnnualBudgetExceeded] = None

    action_if_accumulated_monthly_budget_exceeded: Optional[BudgetActionIfAccumulatedMonthlyBudgetExceeded] = None

    naming_series: BudgetNamingSeries

    applicable_on_cumulative_expense: bool

    action_if_annual_exceeded_on_cumulative_expense: Optional[BudgetActionIfAnnualExceededOnCumulativeExpense] = None

    action_if_accumulated_monthly_exceeded_on_cumulative_expense: Optional[BudgetActionIfAccumulatedMonthlyExceededOnCumulativeExpense] = None

    account_id: uuid.UUID

    budget_amount: Decimal

    revision_of: Optional[str] = None

    distribute_equally: bool

    from_fiscal_year_id: uuid.UUID

    to_fiscal_year_id: uuid.UUID

    budget_start_date: Optional[dt.date] = None

    budget_end_date: Optional[dt.date] = None

    distribution_frequency: BudgetDistributionFrequency

    budget_distribution_total: Optional[Decimal] = None

    budget_distribution: list[BudgetDistributionRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





BudgetListResponse = Page[BudgetRead]

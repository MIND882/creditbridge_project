# HAND-WRITTEN

"""

Business logic for Budget -- port of

``erpnext/accounts/doctype/budget/budget.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks and their ports:

    validate                            -> _validate (orchestrates, same order)

    validate_budget_amount              -> _validate_budget_amount

    validate_fiscal_year                -> _validate_fiscal_years

    set_fiscal_year_dates               -> _set_fiscal_year_dates

    validate_duplicate                  -> _validate_duplicate

    validate_account                    -> _validate_account

    set_null_value                      -> _set_null_value

    validate_applicable_for             -> _validate_applicable_for

    validate_existing_expenses          -> NOT PORTED, see the note below

    before_save / allocate_budget       -> _allocate_budget

    get_budget_periods                  -> _budget_periods

    validate_distribution_totals        -> _validate_distribution_totals



Two upstream concepts collapse here and the code below says where:



* ``company`` became the tenant. ``validate_fiscal_year_company`` checked that the

  company appears in the Fiscal Year's child list; a fiscal year is already

  tenant-scoped, so the equivalent check is that the fiscal year resolves for

  this tenant at all.

* ``validate_duplicate`` joined Fiscal Year to read the window. The window is now

  stored on the budget row itself (``budget_start_date`` / ``budget_end_date``),

  derived from the fiscal years on every save, so the join is unnecessary.



NOT PORTED -- ``validate_existing_expenses`` compares the budget against actual

GL spend and throws "Budget Limit Exceeded". GL Entry is converted but the

budget-to-GL aggregation (cost-centre and project dimensions, the

``against_voucher``/``is_cancelled`` filters, the tree roll-up for a Cost Centre

budget) is a substantial piece of work on its own. Until it lands this rule

fails open: a budget may be saved below what has already been spent. See

``TestExistingExpensesStub``.

"""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal, ROUND_HALF_UP

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.budget_distribution_domain.models.budget_distribution import (

    BudgetDistribution,

)

from app.accounts.budget_domain.models.budget import Budget, BudgetBudgetAgainst

from app.accounts.budget_domain.repositories.budget_repository import (

    BudgetRepository,

)

from app.accounts.budget_domain.schemas.budget import BudgetCreate, BudgetUpdate

from app.accounts.fiscal_year_domain.models.fiscal_year import FiscalYear

from app.core.docstatus import DocStatus, assert_can_cancel, assert_can_submit

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BudgetService"]



#: ``flt(x, 3)`` in Frappe rounds half away from zero.

def _flt(value: Optional[Decimal | float | int], precision: int = 3) -> Decimal:

    quant = Decimal(1).scaleb(-precision)

    return Decimal(str(value if value is not None else 0)).quantize(

        quant, rounding=ROUND_HALF_UP

    )





def _add_months(day: dt.date, months: int) -> dt.date:

    """``frappe.utils.add_months``: clamp the day to the target month's length."""

    total = (day.year * 12 + (day.month - 1)) + months

    year, month = divmod(total, 12)

    month += 1

    last = dt.date(year + (month == 12), 1 if month == 12 else month + 1, 1) - dt.timedelta(days=1)

    return dt.date(year, month, min(day.day, last.day))





_MONTH_INCREMENT = {"Monthly": 1, "Quarterly": 3, "Half-Yearly": 6, "Yearly": 12}

_SPAN_MONTHS = {"Monthly": 0, "Quarterly": 2, "Half-Yearly": 5, "Yearly": 11}





class BudgetService:

    def __init__(self, repository: Optional[BudgetRepository] = None) -> None:

        self.repository = repository or BudgetRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Budget:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Budget", row_id)

        return row



    # ══════════════════════════════════════════════════════════════════════

    # upstream: validate()

    # ══════════════════════════════════════════════════════════════════════

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Budget, *, is_new: bool

    ) -> None:

        # ``validate`` reads the budget_against value off the document.

        self._validate_budget_against(row)

        self._validate_budget_amount(row)

        self._set_fiscal_year_dates(db, business_id, row)

        self._validate_duplicate(db, business_id, row)

        self._validate_account(db, business_id, row)

        self._set_null_value(row)

        self._validate_applicable_for(row)



        # ``before_save`` runs after ``validate`` in Frappe.

        self._allocate_budget(row)

        self._validate_distribution_totals(row)



        self._validate_existing_expenses(db, business_id, row)



    # ── validate(): the scrubbed budget_against field must be populated ────

    def _validate_budget_against(self, row: Budget) -> None:

        against = BudgetBudgetAgainst(row.budget_against).value

        if against == "Cost Center":

            value = row.cost_center_id

        elif against == "Project":

            value = row.project

        else:  # pragma: no cover - the Select has only two options

            value = None

        if not value:

            raise DomainValidationError(

                f"{against} is mandatory",

                code="budget_against_mandatory",

                details={"budget_against": against},

            )



    # ── validate_budget_amount ────────────────────────────────────────────

    def _validate_budget_amount(self, row: Budget) -> None:

        amount = Decimal(row.budget_amount or 0)

        if amount <= 0:

            raise DomainValidationError(

                f"Budget Amount can not be {amount}.",

                code="budget_amount_not_positive",

                details={"budget_amount": str(amount)},

            )



    # ── set_fiscal_year_dates (+ validate_fiscal_year) ────────────────────

    def _set_fiscal_year_dates(

        self, db: Session, business_id: uuid.UUID, row: Budget

    ) -> None:

        """

        The budget window is *copied* from the fiscal years on every save, so a

        client-supplied window cannot drift from them.



        Upstream also ran ``validate_fiscal_year_company``, which required the

        company to be listed on the Fiscal Year. A fiscal year is tenant-scoped

        here, so resolving it for this tenant is the equivalent check.

        """

        start_fy = self._load_fiscal_year(db, business_id, row.from_fiscal_year_id, "from")

        end_fy = self._load_fiscal_year(db, business_id, row.to_fiscal_year_id, "to")



        row.budget_start_date = start_fy.year_start_date

        row.budget_end_date = end_fy.year_end_date



        if row.budget_start_date > row.budget_end_date:

            raise DomainValidationError(

                "From Fiscal Year cannot be greater than To Fiscal Year",

                code="budget_fiscal_year_order",

                details={

                    "from_fiscal_year": start_fy.year,

                    "to_fiscal_year": end_fy.year,

                },

            )



    def _load_fiscal_year(

        self, db: Session, business_id: uuid.UUID, fy_id: Optional[uuid.UUID], which: str

    ) -> FiscalYear:

        fy = (

            db.scalar(

                select(FiscalYear).where(

                    FiscalYear.id == fy_id, FiscalYear.business_id == business_id

                )

            )

            if fy_id

            else None

        )

        if fy is None:

            raise DomainValidationError(

                f"{which.capitalize()} Fiscal Year does not exist for this business",

                code="budget_fiscal_year_not_found",

                details={"fiscal_year_id": str(fy_id) if fy_id else None, "side": which},

            )

        return fy



    # ── validate_duplicate ────────────────────────────────────────────────

    def _validate_duplicate(

        self, db: Session, business_id: uuid.UUID, row: Budget

    ) -> None:

        """

        Another non-cancelled Budget for the same tenant, target and account with

        an overlapping window is a conflict. Cancelled rows are ignored, matching

        upstream's ``docstatus < 2``.

        """

        if not row.account_id:

            return



        against = BudgetBudgetAgainst(row.budget_against).value

        stmt = select(Budget).where(

            Budget.business_id == business_id,

            Budget.account_id == row.account_id,

            Budget.docstatus != DocStatus.CANCELLED.value,

            Budget.budget_against == row.budget_against,

            Budget.budget_start_date <= row.budget_end_date,

            Budget.budget_end_date >= row.budget_start_date,

        )

        if against == "Cost Center":

            stmt = stmt.where(Budget.cost_center_id == row.cost_center_id)

        else:

            stmt = stmt.where(Budget.project == row.project)

        if row.id is not None:

            stmt = stmt.where(Budget.id != row.id)



        existing = db.scalars(stmt).first()

        if existing is not None:

            target = row.cost_center_id or row.project

            raise DomainValidationError(

                f"Another Budget record '{existing.name}' already exists against "

                f"{against} '{target}' and account '{row.account_id}' with "

                f"overlapping fiscal years.",

                code="budget_duplicate",

                details={"existing_budget": existing.name},

            )



    # ── validate_account ──────────────────────────────────────────────────

    def _validate_account(

        self, db: Session, business_id: uuid.UUID, row: Budget

    ) -> None:

        if not row.account_id:

            raise DomainValidationError(

                "Account is mandatory", code="budget_account_mandatory"

            )



        account = db.scalar(

            select(Account).where(

                Account.id == row.account_id, Account.business_id == business_id

            )

        )

        if account is None:

            # Upstream would KeyError on a missing cached doc; a 400 is the

            # honest equivalent, and it also covers "belongs to another tenant".

            raise DomainValidationError(

                f"Account {row.account_id} does not belong to this business",

                code="budget_account_not_found",

                details={"account_id": str(row.account_id)},

            )



        if account.is_group:

            raise DomainValidationError(

                f"Budget cannot be assigned against Group Account {account.name}",

                code="budget_account_is_group",

                details={"account": account.name},

            )



        report_type = getattr(account.report_type, "value", account.report_type)

        if report_type != "Profit and Loss":

            raise DomainValidationError(

                f"Budget cannot be assigned against {account.name}, as its Root "

                f"Type is not of Income or Expense",

                code="budget_account_not_pl",

                details={"account": account.name, "report_type": str(report_type)},

            )



    # ── set_null_value ────────────────────────────────────────────────────

    def _set_null_value(self, row: Budget) -> None:

        if BudgetBudgetAgainst(row.budget_against).value == "Cost Center":

            row.project = None

        else:

            row.cost_center_id = None



    # ── validate_applicable_for ───────────────────────────────────────────

    def _validate_applicable_for(self, row: Budget) -> None:

        if row.applicable_on_material_request and not (

            row.applicable_on_purchase_order and row.applicable_on_booking_actual_expenses

        ):

            raise DomainValidationError(

                "Please enable Applicable on Purchase Order and Applicable on "

                "Booking Actual Expenses",

                code="budget_applicable_on_mr",

            )



        if row.applicable_on_purchase_order and not row.applicable_on_booking_actual_expenses:

            raise DomainValidationError(

                "Please enable Applicable on Booking Actual Expenses",

                code="budget_applicable_on_po",

            )



        if not (

            row.applicable_on_material_request

            or row.applicable_on_purchase_order

            or row.applicable_on_booking_actual_expenses

        ):

            # Upstream does not throw here -- it defaults the flag on.

            row.applicable_on_booking_actual_expenses = True



    # ── validate_existing_expenses ────────────────────────────────────────

    def _validate_existing_expenses(

        self, db: Session, business_id: uuid.UUID, row: Budget

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream compares this budget against what has

        already been posted to GL for the same account, window and target, and

        throws "Budget Limit Exceeded" when actual spend is already above the

        new figure.



        NOT PORTED -- this fails open, so a budget may currently be saved below

        what has already been spent. What is missing is the GL Entry

        aggregation itself: summing credit/debit by account within

        [budget_start_date, budget_end_date], restricted to the budget's cost

        centre or project, honouring ``is_cancelled`` and rolling a Cost Centre

        budget up over its subtree. GL Entry is converted; the query is not

        written. See ``TestExistingExpensesStub``.

        """

        return None



    # ══════════════════════════════════════════════════════════════════════

    # upstream: before_save() -> allocate_budget()

    # ══════════════════════════════════════════════════════════════════════

    def _allocate_budget(self, row: Budget) -> None:

        if self._should_regenerate(row):

            self._regenerate_distribution(row)

        row.budget_distribution_total = sum(

            (_flt(d.amount) for d in row.budget_distribution), Decimal(0)

        )



    def _should_regenerate(self, row: Budget) -> bool:

        """

        ``should_regenerate_budget_distribution``. A manual split is only

        regenerated when the user asked for an even one, or when there is no

        split to preserve.

        """

        if not row.budget_distribution:

            return True

        return bool(row.distribute_equally)



    def _budget_periods(self, row: Budget) -> list[tuple[dt.date, dt.date]]:

        freq = str(

            getattr(row.distribution_frequency, "value", row.distribution_frequency)

        )

        increment = _MONTH_INCREMENT.get(freq, 1)

        span = _SPAN_MONTHS.get(freq, 0)



        periods: list[tuple[dt.date, dt.date]] = []

        cursor = row.budget_start_date.replace(day=1)

        while cursor <= row.budget_end_date:

            end = _add_months(cursor, span)

            # last day of that month

            end = (

                dt.date(end.year + (end.month == 12), 1 if end.month == 12 else end.month + 1, 1)

                - dt.timedelta(days=1)

            )

            periods.append((cursor, min(end, row.budget_end_date)))

            cursor = _add_months(cursor, increment)

        return periods



    def _regenerate_distribution(self, row: Budget) -> None:

        row.budget_distribution.clear()



        periods = self._budget_periods(row)

        if not periods:

            return



        # ``add_allocated_amount`` takes the *unrounded* share and rounds only

        # what it stores. Rounding the share first drifts: 120000/12 stored as

        # 8.333 and then applied gives 9999.6 per row instead of 10000.

        row_percent = Decimal(100) / Decimal(len(periods))

        amount = _flt(Decimal(row.budget_amount) * row_percent / Decimal(100))

        stored_percent = _flt(row_percent)



        for idx, (start, end) in enumerate(periods, start=1):

            row.budget_distribution.append(

                BudgetDistribution(

                    business_id=row.business_id,

                    idx=idx,

                    start_date=start,

                    end_date=end,

                    amount=amount,

                    percent=stored_percent,

                )

            )



    # ── on_update -> validate_distribution_totals ─────────────────────────

    def _validate_distribution_totals(self, row: Budget) -> None:

        if self._should_regenerate(row):

            return



        total_amount = sum((_flt(d.amount) for d in row.budget_distribution), Decimal(0))

        total_percent = sum((_flt(d.percent) for d in row.budget_distribution), Decimal(0))



        if abs(total_amount - Decimal(row.budget_amount)) > Decimal("0.10"):

            raise DomainValidationError(

                f"Total distributed amount {total_amount} must be equal to "

                f"Budget Amount {row.budget_amount}",

                code="budget_distribution_amount",

                details={"total": str(total_amount)},

            )



        if abs(total_percent - Decimal(100)) > Decimal("0.10"):

            raise DomainValidationError(

                f"Total distribution percent must equal 100 (currently {total_percent})",

                code="budget_distribution_percent",

                details={"total": str(total_percent)},

            )



    # ══════════════════════════════════════════════════════════════════════

    # public API

    # ══════════════════════════════════════════════════════════════════════

    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Budget:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Budget]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Budget].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_budget_distribution(

        self, business_id: uuid.UUID, row: Budget, items: list[dict]

    ) -> None:

        row.budget_distribution.clear()

        for idx, item in enumerate(items, start=1):

            row.budget_distribution.append(

                BudgetDistribution(

                    business_id=business_id,

                    idx=idx,

                    start_date=item.get("start_date"),

                    end_date=item.get("end_date"),

                    amount=item.get("amount"),

                    percent=item.get("percent"),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """

        Upstream ``autoname`` is ``naming_series:`` with the single option

        ``BUDGET-.########``, so names are ``BUDGET-00000001`` and up.

        """

        count = int(

            db.scalar(

                select(func.count()).select_from(Budget).where(

                    Budget.business_id == business_id

                )

            )

            or 0

        )

        return f"BUDGET-{count + 1:08d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BudgetCreate

    ) -> Budget:

        row = Budget(

            business_id=business_id,

            name=self.next_name(db, business_id),

            budget_against=payload.budget_against,

            cost_center_id=payload.cost_center_id,

            project=payload.project,

            amended_from=payload.amended_from,

            applicable_on_material_request=payload.applicable_on_material_request,

            action_if_annual_budget_exceeded_on_mr=payload.action_if_annual_budget_exceeded_on_mr,

            action_if_accumulated_monthly_budget_exceeded_on_mr=payload.action_if_accumulated_monthly_budget_exceeded_on_mr,

            applicable_on_purchase_order=payload.applicable_on_purchase_order,

            action_if_annual_budget_exceeded_on_po=payload.action_if_annual_budget_exceeded_on_po,

            action_if_accumulated_monthly_budget_exceeded_on_po=payload.action_if_accumulated_monthly_budget_exceeded_on_po,

            applicable_on_booking_actual_expenses=payload.applicable_on_booking_actual_expenses,

            action_if_annual_budget_exceeded=payload.action_if_annual_budget_exceeded,

            action_if_accumulated_monthly_budget_exceeded=payload.action_if_accumulated_monthly_budget_exceeded,

            naming_series=payload.naming_series,

            applicable_on_cumulative_expense=payload.applicable_on_cumulative_expense,

            action_if_annual_exceeded_on_cumulative_expense=payload.action_if_annual_exceeded_on_cumulative_expense,

            action_if_accumulated_monthly_exceeded_on_cumulative_expense=payload.action_if_accumulated_monthly_exceeded_on_cumulative_expense,

            account_id=payload.account_id,

            budget_amount=payload.budget_amount,

            revision_of=payload.revision_of,

            distribute_equally=payload.distribute_equally,

            from_fiscal_year_id=payload.from_fiscal_year_id,

            to_fiscal_year_id=payload.to_fiscal_year_id,

            budget_start_date=payload.budget_start_date,

            budget_end_date=payload.budget_end_date,

            distribution_frequency=payload.distribution_frequency,

            budget_distribution_total=payload.budget_distribution_total,

        )

        self._replace_budget_distribution(

            business_id, row, [x.model_dump() for x in payload.budget_distribution]

        )



        try:

            db.flush()  # children need ids before validation reads them

            self._validate(db, business_id, row, is_new=True)

            self.repository.add(db, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        row_id: uuid.UUID,

        payload: BudgetUpdate,

    ) -> Budget:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "budget_distribution":

                    self._replace_budget_distribution(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row, is_new=False)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, row_id)

        self.repository.delete(db, row)

        db.commit()



    def submit(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Budget:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Budget")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Budget:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Budget")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

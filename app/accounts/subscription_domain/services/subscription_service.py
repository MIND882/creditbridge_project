# HAND-WRITTEN

"""

Business logic for Subscription -- port of

``erpnext/accounts/doctype/subscription/subscription.py``.







Upstream hooks:

    before_insert

    after_insert

    generate_invoices_till_date

    update_subscription_period

    get_current_invoice_start

    get_current_invoice_end

    validate_plans_billing_cycle

    get_billing_cycle_and_interval

    get_billing_cycle_data

    set_subscription_status

    is_trialling

    period_has_passed

    get_status_for_past_grace_period

    is_past_grace_period

    current_invoice_is_past_due

    invoice_document_type

    validate

    validate_party_billing_currency

    validate_trial_period

    validate_end_date

    validate_to_follow_calendar_months

    generate_invoice

    create_invoice

    get_items_from_plans

    process

    can_generate_new_invoice

    is_current_invoice_generated

    current_invoice

    get_current_invoice

    invoices

    is_paid

    has_outstanding_invoice

    is_fully_refunded

    cancel_subscription

    restart_subscription

    force_fetch_subscription_updates

    get_billing_heatmap



Seven of the eleven upstream ``frappe.throw`` sites are ported -- the trial

period ordering, the single-billing-cycle rule, the end-date check and the

calendar-month rules. ``validate_party_billing_currency`` is not, and says

why; see :meth:`_validate`.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



import datetime as dt



from app.accounts.subscription_domain.models.subscription import Subscription

from app.accounts.subscription_plan_domain.models.subscription_plan import (

    SubscriptionPlan,

)

from app.accounts.subscription_plan_detail_domain.models.subscription_plan_detail import SubscriptionPlanDetail

from app.accounts.subscription_domain.repositories.subscription_repository import (

    SubscriptionRepository,

)

from app.accounts.subscription_domain.schemas.subscription import (

    SubscriptionCreate,

    SubscriptionUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SubscriptionService"]





def _add_months(day: dt.date, months: int) -> dt.date:

    """Add whole months, clamping the day to the target month's length."""

    total = day.year * 12 + (day.month - 1) + months

    year, month = divmod(total, 12)

    month += 1

    nxt = dt.date(year + (month == 12), 1 if month == 12 else month + 1, 1)

    return dt.date(year, month, min(day.day, (nxt - dt.timedelta(days=1)).day))





class SubscriptionService:

    def __init__(self, repository: Optional[SubscriptionRepository] = None) -> None:

        self.repository = repository or SubscriptionRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Subscription:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Subscription", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    # ══════════════════════════════════════════════════════════════════════

    # ported validators

    # ══════════════════════════════════════════════════════════════════════

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Subscription

    ) -> None:

        """

        Port of upstream ``validate``. Seven of its eleven ``frappe.throw`` sites

        are enforced:



            validate_trial_period               -> ported (3 throws)

            validate_plans_billing_cycle        -> ported (1 throw)

            validate_end_date                   -> ported (1 throw)

            validate_to_follow_calendar_months  -> ported (2 throws)



        Upstream also defaults ``cost_center`` from the Company and calls

        ``set_subscription_status`` on new rows. Neither is ported: ``Company``

        is not converted (the tenant is ``business_id`` and has no default cost

        centre), and the status machine reads invoice and payment state that

        lives outside this module.



        TODO(PORT-VALIDATION): ``validate_party_billing_currency`` is not ported.

        It rejects plans whose currency differs from the party's default billing

        currency, which is stored on Customer/Supplier. Neither doctype is

        converted, so there is nothing to compare against and the check fails

        open -- a subscription may be created with plans in a currency the party

        cannot be billed in.

        """

        self._validate_trial_period(row)

        self._validate_plans_billing_cycle(db, business_id, row)

        self._validate_end_date(db, business_id, row)

        self._validate_to_follow_calendar_months(db, business_id, row)



    # ── validate_trial_period ─────────────────────────────────────────────

    def _validate_trial_period(self, row: Subscription) -> None:

        """

        Three ordering rules. Note the asymmetry upstream carries: a start

        without an end is an error, but an end without a start is not -- a

        missing start simply means there is no trial.

        """

        if row.trial_period_start and row.trial_period_end:

            if row.trial_period_end < row.trial_period_start:

                raise DomainValidationError(

                    "Trial Period End Date Cannot be before Trial Period Start Date",

                    code="subscription_trial_end_before_start",

                    details={

                        "trial_period_start": row.trial_period_start.isoformat(),

                        "trial_period_end": row.trial_period_end.isoformat(),

                    },

                )



        if row.trial_period_start and not row.trial_period_end:

            raise DomainValidationError(

                "Both Trial Period Start Date and Trial Period End Date must be set",

                code="subscription_trial_needs_both_dates",

                details={"trial_period_start": row.trial_period_start.isoformat()},

            )



        if row.trial_period_start and row.start_date and row.trial_period_start > row.start_date:

            raise DomainValidationError(

                "Trial Period Start date cannot be after Subscription Start Date",

                code="subscription_trial_after_start",

                details={

                    "trial_period_start": row.trial_period_start.isoformat(),

                    "start_date": row.start_date.isoformat(),

                },

            )



    # ── validate_plans_billing_cycle ──────────────────────────────────────

    def _validate_plans_billing_cycle(

        self, db: Session, business_id: uuid.UUID, row: Subscription

    ) -> None:

        """

        A subscription bills on one cycle, so every plan on it must agree.



        Upstream selects DISTINCT (billing_interval, billing_interval_count), so

        a 1-month and a 3-month plan are two different cycles even though both

        are "Month".

        """

        cycles = self._billing_cycles(db, business_id, row)

        if cycles and len(cycles) != 1:

            raise DomainValidationError(

                "You can only have Plans with the same billing cycle in a Subscription",

                code="subscription_mixed_billing_cycle",

                details={"cycles": [list(c) for c in sorted(cycles)]},

            )



    # ── validate_end_date ─────────────────────────────────────────────────

    def _validate_end_date(

        self, db: Session, business_id: uuid.UUID, row: Subscription

    ) -> None:

        """

        The end date must leave room for at least one full billing period, or

        the first invoice would be cut short.

        """

        if not row.plans or not row.start_date or not row.end_date:

            return



        cycle_end = self._cycle_end_date(db, business_id, row)

        if cycle_end is None:

            return



        if row.end_date <= cycle_end:

            raise DomainValidationError(

                f"Subscription End Date must be after {cycle_end.isoformat()} "

                f"as per the subscription plan",

                code="subscription_end_date_too_early",

                details={

                    "end_date": row.end_date.isoformat(),

                    "must_be_after": cycle_end.isoformat(),

                },

            )



    # ── validate_to_follow_calendar_months ────────────────────────────────

    def _validate_to_follow_calendar_months(

        self, db: Session, business_id: uuid.UUID, row: Subscription

    ) -> None:

        if not row.follow_calendar_months:

            return



        if not row.end_date:

            raise DomainValidationError(

                "Subscription End Date is mandatory to follow calendar months",

                code="subscription_calendar_months_needs_end_date",

            )



        cycles = self._billing_cycles(db, business_id, row)

        if cycles and next(iter(cycles))[0] != "Month":

            raise DomainValidationError(

                "Billing Interval in Subscription Plan must be Month to follow "

                "calendar months",

                code="subscription_calendar_months_needs_month_interval",

                details={"billing_interval": next(iter(cycles))[0]},

            )



    # ── billing cycle lookups ─────────────────────────────────────────────

    def _billing_cycles(

        self, db: Session, business_id: uuid.UUID, row: Subscription

    ) -> set[tuple[str, int]]:

        """

        The distinct (interval, count) pairs across this subscription's plans.



        Plan rows reference ``SubscriptionPlan`` by name, and names are unique

        per tenant, so the lookup is scoped by both.

        """

        names = [c.plan for c in row.plans if c.plan]

        if not names:

            return set()

        pairs = db.execute(

            select(

                SubscriptionPlan.billing_interval,

                SubscriptionPlan.billing_interval_count,

            )

            .where(

                SubscriptionPlan.business_id == business_id,

                SubscriptionPlan.name.in_(names),

            )

            .distinct()

        ).all()

        return {(getattr(i, "value", i), int(c or 0)) for i, c in pairs}



    def _cycle_end_date(

        self, db: Session, business_id: uuid.UUID, row: Subscription

    ) -> Optional[dt.date]:

        """

        Port of ``get_billing_cycle_data`` applied to ``start_date``.



        Upstream builds a kwargs dict for ``add_to_date``: Day and Week map to a

        day count (``count - 1`` and ``count * 7 - 1``), while Month and Year

        carry ``days = -1`` alongside the interval so the period ends on the last

        day before the next one begins.

        """

        cycles = self._billing_cycles(db, business_id, row)

        if not cycles:

            return None

        interval, count = next(iter(cycles))



        if interval == "Day":

            return row.start_date + dt.timedelta(days=count - 1)

        if interval == "Week":

            return row.start_date + dt.timedelta(days=count * 7 - 1)

        if interval == "Month":

            return _add_months(row.start_date, count) - dt.timedelta(days=1)

        if interval == "Year":

            return _add_months(row.start_date, count * 12) - dt.timedelta(days=1)

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Subscription:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Subscription]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Subscription].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_plans(

        self, business_id: uuid.UUID, row: Subscription, items: list[dict]

    ) -> None:

        row.plans.clear()

        for idx, item in enumerate(items, start=1):

            row.plans.append(

                SubscriptionPlanDetail(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Subscription',

                    qty=item.get('qty'),

                    plan=item.get('plan'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(Subscription).where(

                    Subscription.business_id == business_id

                )

            )

            or 0

        )

        return f"SUB-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SubscriptionCreate

    ) -> Subscription:

        row = Subscription(

            business_id=business_id,

            name=self.next_name(db, business_id),

            status=payload.status,

            cancelation_date=payload.cancelation_date,

            trial_period_start=payload.trial_period_start,

            trial_period_end=payload.trial_period_end,

            current_invoice_start=payload.current_invoice_start,

            current_invoice_end=payload.current_invoice_end,

            next_billing_period_start=payload.next_billing_period_start,

            next_billing_period_end=payload.next_billing_period_end,

            days_until_due=payload.days_until_due,

            cancel_at_period_end=payload.cancel_at_period_end,

            apply_additional_discount=payload.apply_additional_discount,

            additional_discount_percentage=payload.additional_discount_percentage,

            additional_discount_amount=payload.additional_discount_amount,

            party_type=payload.party_type,

            party=payload.party,

            sales_tax_template=payload.sales_tax_template,

            purchase_tax_template=payload.purchase_tax_template,

            follow_calendar_months=payload.follow_calendar_months,

            generate_new_invoices_past_due_date=payload.generate_new_invoices_past_due_date,

            end_date=payload.end_date,

            start_date=payload.start_date,

            cost_center_id=payload.cost_center_id,

            submit_invoice=payload.submit_invoice,

            generate_invoice_at=payload.generate_invoice_at,

            number_of_days=payload.number_of_days,

        )

        self._replace_plans(business_id, row, [x.model_dump() for x in payload.plans])



        try:

            db.flush()  # children need ids before validation reads them

            self._validate(db, business_id, row)

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

        payload: SubscriptionUpdate,

    ) -> Subscription:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "plans":

                    self._replace_plans(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row)

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

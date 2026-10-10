# HAND-WRITTEN

"""

Business logic for Subscription Plan -- port of

``erpnext/accounts/doctype/subscription_plan/subscription_plan.py``.







Upstream hooks:

    validate

    validate_interval_count



**Upstream has 1 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.subscription_plan_domain.models.subscription_plan import SubscriptionPlan

from app.accounts.subscription_plan_domain.repositories.subscription_plan_repository import (

    SubscriptionPlanRepository,

)

from app.accounts.subscription_plan_domain.schemas.subscription_plan import (

    SubscriptionPlanCreate,

    SubscriptionPlanUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SubscriptionPlanService"]





class SubscriptionPlanService:

    def __init__(self, repository: Optional[SubscriptionPlanRepository] = None) -> None:

        self.repository = repository or SubscriptionPlanRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SubscriptionPlan:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Subscription Plan", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SubscriptionPlan

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **1 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SubscriptionPlan:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SubscriptionPlan]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SubscriptionPlan].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(SubscriptionPlan).where(

                    SubscriptionPlan.business_id == business_id

                )

            )

            or 0

        )

        return f"SUB-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SubscriptionPlanCreate

    ) -> SubscriptionPlan:

        row = SubscriptionPlan(

            business_id=business_id,

            name=self.next_name(db, business_id),

            plan_name=payload.plan_name,

            currency=payload.currency,

            item=payload.item,

            price_determination=payload.price_determination,

            cost=payload.cost,

            price_list=payload.price_list,

            billing_interval=payload.billing_interval,

            billing_interval_count=payload.billing_interval_count,

            payment_gateway=payload.payment_gateway,

            cost_center_id=payload.cost_center_id,

        )



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

        payload: SubscriptionPlanUpdate,

    ) -> SubscriptionPlan:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

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

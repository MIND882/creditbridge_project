# HAND-WRITTEN

"""

Business logic for Monthly Distribution -- port of

``erpnext/accounts/doctype/monthly_distribution/monthly_distribution.py``.







Upstream hooks:

    get_months

    validate



**Upstream has 1 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.monthly_distribution_domain.models.monthly_distribution import MonthlyDistribution

from app.accounts.monthly_distribution_percentage_domain.models.monthly_distribution_percentage import MonthlyDistributionPercentage

from app.accounts.monthly_distribution_domain.repositories.monthly_distribution_repository import (

    MonthlyDistributionRepository,

)

from app.accounts.monthly_distribution_domain.schemas.monthly_distribution import (

    MonthlyDistributionCreate,

    MonthlyDistributionUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["MonthlyDistributionService"]





class MonthlyDistributionService:

    def __init__(self, repository: Optional[MonthlyDistributionRepository] = None) -> None:

        self.repository = repository or MonthlyDistributionRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> MonthlyDistribution:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Monthly Distribution", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: MonthlyDistribution

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

    ) -> MonthlyDistribution:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[MonthlyDistribution]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[MonthlyDistribution].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_percentages(

        self, business_id: uuid.UUID, row: MonthlyDistribution, items: list[dict]

    ) -> None:

        row.percentages.clear()

        for idx, item in enumerate(items, start=1):

            row.percentages.append(

                MonthlyDistributionPercentage(

                    business_id=business_id,

                    idx=idx,

                    name=item.get('name'),

                    month=item.get('month'),

                    percentage_allocation=item.get('percentage_allocation'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(MonthlyDistribution).where(

                    MonthlyDistribution.business_id == business_id

                )

            )

            or 0

        )

        return f"MON-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: MonthlyDistributionCreate

    ) -> MonthlyDistribution:

        row = MonthlyDistribution(

            business_id=business_id,

            name=self.next_name(db, business_id),

            fiscal_year_id=payload.fiscal_year_id,

        )

        self._replace_percentages(business_id, row, [x.model_dump() for x in payload.percentages])



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

        payload: MonthlyDistributionUpdate,

    ) -> MonthlyDistribution:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "percentages":

                    self._replace_percentages(business_id, row, value or [])

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

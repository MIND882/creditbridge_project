"""Business logic for Supplier Scorecard Period -- port of

``erpnext/buying/doctype/supplier_scorecard_period/supplier_scorecard_period.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_period_domain.models.supplier_scorecard_period import SupplierScorecardPeriod

from app.buying.supplier_scorecard_period_domain.repositories.supplier_scorecard_period_repository import (

    SupplierScorecardPeriodRepository,

)

from app.buying.supplier_scorecard_period_domain.schemas.supplier_scorecard_period import (

    SupplierScorecardPeriodCreate,

    SupplierScorecardPeriodUpdate,

)

from app.buying.supplier_scorecard_scoring_variable_domain.models.supplier_scorecard_scoring_variable import SupplierScorecardScoringVariable

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierScorecardPeriodService"]





class SupplierScorecardPeriodService:

    def __init__(self, repository: Optional[SupplierScorecardPeriodRepository] = None) -> None:

        self.repository = repository or SupplierScorecardPeriodRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardPeriod:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Scorecard Period", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SupplierScorecardPeriod

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardPeriod:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierScorecardPeriod]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierScorecardPeriod].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID, series: Optional[str] = None) -> str:

        """A per-tenant sequential name; upstream mints one from ``naming_series``."""

        # ``naming_series`` is optional on input (Frappe fills it from a

        # default), so fall back to the doctype prefix when it is absent.

        series = series or ""

        prefix = series.split(".")[0].split("#")[0]

        if prefix and not prefix.endswith("-"):

            prefix += "-"

        count = int(

            db.scalar(

                select(func.count()).select_from(SupplierScorecardPeriod).where(

                    SupplierScorecardPeriod.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SupplierScorecardPeriodCreate

    ) -> SupplierScorecardPeriod:

        row = SupplierScorecardPeriod(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            supplier_id=payload.supplier_id,

            naming_series=payload.naming_series,

            total_score=payload.total_score,

            start_date=payload.start_date,

            end_date=payload.end_date,

            scorecard_id=payload.scorecard_id,

            amended_from_id=payload.amended_from_id,

        )

        self._replace_variables(business_id, row, [x.model_dump() for x in payload.variables])



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

        payload: SupplierScorecardPeriodUpdate,

    ) -> SupplierScorecardPeriod:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "variables":

                    self._replace_variables(business_id, row, value or [])

                    continue

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



    def _replace_variables(

        self, business_id: uuid.UUID, row: SupplierScorecardPeriod, variables: list[dict]

    ) -> None:

        row.variables.clear()

        for idx, entry in enumerate(variables, start=1):

            row.variables.append(

                SupplierScorecardScoringVariable(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Supplier Scorecard Period",

                    parentfield="variables",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )

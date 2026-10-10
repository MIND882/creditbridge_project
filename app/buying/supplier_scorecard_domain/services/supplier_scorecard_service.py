"""Business logic for Supplier Scorecard -- port of

``erpnext/buying/doctype/supplier_scorecard/supplier_scorecard.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_domain.models.supplier_scorecard import SupplierScorecard

from app.buying.supplier_scorecard_domain.repositories.supplier_scorecard_repository import (

    SupplierScorecardRepository,

)

from app.buying.supplier_scorecard_domain.schemas.supplier_scorecard import (

    SupplierScorecardCreate,

    SupplierScorecardUpdate,

)

from app.buying.supplier_scorecard_scoring_standing_domain.models.supplier_scorecard_scoring_standing import SupplierScorecardScoringStanding

from app.buying.supplier_scorecard_scoring_criteria_domain.models.supplier_scorecard_scoring_criteria import SupplierScorecardScoringCriteria

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierScorecardService"]





class SupplierScorecardService:

    def __init__(self, repository: Optional[SupplierScorecardRepository] = None) -> None:

        self.repository = repository or SupplierScorecardRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecard:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Scorecard", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SupplierScorecard

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecard:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierScorecard]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierScorecard].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:supplier'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SupplierScorecardCreate

    ) -> SupplierScorecard:

        row = SupplierScorecard(

            business_id=business_id,

            name=str(payload.supplier_id),

            supplier_id=payload.supplier_id,

            supplier_score=payload.supplier_score,

            indicator_color=payload.indicator_color,

            status=payload.status,

            period=payload.period,

            weighting_function=payload.weighting_function,

            warn_rfqs=payload.warn_rfqs,

            warn_pos=payload.warn_pos,

            prevent_rfqs=payload.prevent_rfqs,

            prevent_pos=payload.prevent_pos,

            notify_supplier=payload.notify_supplier,

            notify_employee=payload.notify_employee,

            employee=payload.employee,

        )

        self._replace_standings(business_id, row, [x.model_dump() for x in payload.standings])

        self._replace_criteria(business_id, row, [x.model_dump() for x in payload.criteria])



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

        payload: SupplierScorecardUpdate,

    ) -> SupplierScorecard:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "standings":

                    self._replace_standings(business_id, row, value or [])

                    continue

                if field_name == "criteria":

                    self._replace_criteria(business_id, row, value or [])

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



    def _replace_standings(

        self, business_id: uuid.UUID, row: SupplierScorecard, standings: list[dict]

    ) -> None:

        row.standings.clear()

        for idx, entry in enumerate(standings, start=1):

            row.standings.append(

                SupplierScorecardScoringStanding(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Supplier Scorecard",

                    parentfield="standings",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_criteria(

        self, business_id: uuid.UUID, row: SupplierScorecard, criteria: list[dict]

    ) -> None:

        row.criteria.clear()

        for idx, entry in enumerate(criteria, start=1):

            row.criteria.append(

                SupplierScorecardScoringCriteria(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Supplier Scorecard",

                    parentfield="criteria",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )

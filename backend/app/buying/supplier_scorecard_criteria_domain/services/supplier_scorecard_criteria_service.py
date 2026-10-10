"""Business logic for Supplier Scorecard Criteria -- port of

``erpnext/buying/doctype/supplier_scorecard_criteria/supplier_scorecard_criteria.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_criteria_domain.models.supplier_scorecard_criteria import SupplierScorecardCriteria

from app.buying.supplier_scorecard_criteria_domain.repositories.supplier_scorecard_criteria_repository import (

    SupplierScorecardCriteriaRepository,

)

from app.buying.supplier_scorecard_criteria_domain.schemas.supplier_scorecard_criteria import (

    SupplierScorecardCriteriaCreate,

    SupplierScorecardCriteriaUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierScorecardCriteriaService"]





class SupplierScorecardCriteriaService:

    def __init__(self, repository: Optional[SupplierScorecardCriteriaRepository] = None) -> None:

        self.repository = repository or SupplierScorecardCriteriaRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardCriteria:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Scorecard Criteria", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SupplierScorecardCriteria

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardCriteria:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierScorecardCriteria]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierScorecardCriteria].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:criteria_name'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SupplierScorecardCriteriaCreate

    ) -> SupplierScorecardCriteria:

        row = SupplierScorecardCriteria(

            business_id=business_id,

            name=payload.criteria_name,

            criteria_name=payload.criteria_name,

            max_score=payload.max_score,

            formula=payload.formula,

            weight=payload.weight,

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

        payload: SupplierScorecardCriteriaUpdate,

    ) -> SupplierScorecardCriteria:

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

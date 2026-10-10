"""Business logic for Supplier Scorecard Variable -- port of

``erpnext/buying/doctype/supplier_scorecard_variable/supplier_scorecard_variable.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_variable_domain.models.supplier_scorecard_variable import SupplierScorecardVariable

from app.buying.supplier_scorecard_variable_domain.repositories.supplier_scorecard_variable_repository import (

    SupplierScorecardVariableRepository,

)

from app.buying.supplier_scorecard_variable_domain.schemas.supplier_scorecard_variable import (

    SupplierScorecardVariableCreate,

    SupplierScorecardVariableUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierScorecardVariableService"]





class SupplierScorecardVariableService:

    def __init__(self, repository: Optional[SupplierScorecardVariableRepository] = None) -> None:

        self.repository = repository or SupplierScorecardVariableRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardVariable:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Scorecard Variable", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SupplierScorecardVariable

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardVariable:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierScorecardVariable]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierScorecardVariable].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:variable_label'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SupplierScorecardVariableCreate

    ) -> SupplierScorecardVariable:

        row = SupplierScorecardVariable(

            business_id=business_id,

            name=payload.variable_label,

            variable_label=payload.variable_label,

            is_custom=payload.is_custom,

            param_name=payload.param_name,

            path=payload.path,

            description=payload.description,

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

        payload: SupplierScorecardVariableUpdate,

    ) -> SupplierScorecardVariable:

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

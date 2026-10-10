"""Business logic for Supplier Scorecard Standing -- port of

``erpnext/buying/doctype/supplier_scorecard_standing/supplier_scorecard_standing.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_standing_domain.models.supplier_scorecard_standing import SupplierScorecardStanding

from app.buying.supplier_scorecard_standing_domain.repositories.supplier_scorecard_standing_repository import (

    SupplierScorecardStandingRepository,

)

from app.buying.supplier_scorecard_standing_domain.schemas.supplier_scorecard_standing import (

    SupplierScorecardStandingCreate,

    SupplierScorecardStandingUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierScorecardStandingService"]





class SupplierScorecardStandingService:

    def __init__(self, repository: Optional[SupplierScorecardStandingRepository] = None) -> None:

        self.repository = repository or SupplierScorecardStandingRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardStanding:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Scorecard Standing", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SupplierScorecardStanding

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardStanding:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierScorecardStanding]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierScorecardStanding].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:standing_name'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SupplierScorecardStandingCreate

    ) -> SupplierScorecardStanding:

        row = SupplierScorecardStanding(

            business_id=business_id,

            name=payload.standing_name,

            standing_name=payload.standing_name,

            standing_color=payload.standing_color,

            min_grade=payload.min_grade,

            max_grade=payload.max_grade,

            warn_rfqs=payload.warn_rfqs,

            warn_pos=payload.warn_pos,

            prevent_rfqs=payload.prevent_rfqs,

            prevent_pos=payload.prevent_pos,

            notify_supplier=payload.notify_supplier,

            notify_employee=payload.notify_employee,

            employee_link=payload.employee_link,

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

        payload: SupplierScorecardStandingUpdate,

    ) -> SupplierScorecardStanding:

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

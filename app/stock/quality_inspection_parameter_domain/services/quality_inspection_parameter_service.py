"""Business logic for Quality Inspection Parameter -- port of

``erpnext/stock/doctype/quality_inspection_parameter/quality_inspection_parameter.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.quality_inspection_parameter_domain.models.quality_inspection_parameter import QualityInspectionParameter

from app.stock.quality_inspection_parameter_domain.repositories.quality_inspection_parameter_repository import (

    QualityInspectionParameterRepository,

)

from app.stock.quality_inspection_parameter_domain.schemas.quality_inspection_parameter import (

    QualityInspectionParameterCreate,

    QualityInspectionParameterUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["QualityInspectionParameterService"]





class QualityInspectionParameterService:

    def __init__(self, repository: Optional[QualityInspectionParameterRepository] = None) -> None:

        self.repository = repository or QualityInspectionParameterRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> QualityInspectionParameter:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Quality Inspection Parameter", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: QualityInspectionParameter

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> QualityInspectionParameter:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[QualityInspectionParameter]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[QualityInspectionParameter].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:parameter'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: QualityInspectionParameterCreate

    ) -> QualityInspectionParameter:

        row = QualityInspectionParameter(

            business_id=business_id,

            name=payload.parameter,

            parameter=payload.parameter,

            description=payload.description,

            parameter_group_id=payload.parameter_group_id,

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

        payload: QualityInspectionParameterUpdate,

    ) -> QualityInspectionParameter:

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

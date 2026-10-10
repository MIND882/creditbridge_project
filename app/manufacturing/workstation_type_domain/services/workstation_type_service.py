"""Business logic for Workstation Type -- port of

``erpnext/manufacturing/doctype/workstation_type/workstation_type.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.workstation_type_domain.models.workstation_type import WorkstationType

from app.manufacturing.workstation_type_domain.repositories.workstation_type_repository import (

    WorkstationTypeRepository,

)

from app.manufacturing.workstation_type_domain.schemas.workstation_type import (

    WorkstationTypeCreate,

    WorkstationTypeUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["WorkstationTypeService"]





class WorkstationTypeService:

    def __init__(self, repository: Optional[WorkstationTypeRepository] = None) -> None:

        self.repository = repository or WorkstationTypeRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkstationType:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Workstation Type", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: WorkstationType

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkstationType:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[WorkstationType]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[WorkstationType].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:workstation_type'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: WorkstationTypeCreate

    ) -> WorkstationType:

        row = WorkstationType(

            business_id=business_id,

            name=payload.workstation_type,

            workstation_type=payload.workstation_type,

            hour_rate=payload.hour_rate,

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

        payload: WorkstationTypeUpdate,

    ) -> WorkstationType:

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

"""Business logic for Industry Type -- port of

``erpnext/selling/doctype/industry_type/industry_type.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.industry_type_domain.models.industry_type import IndustryType

from app.selling.industry_type_domain.repositories.industry_type_repository import (

    IndustryTypeRepository,

)

from app.selling.industry_type_domain.schemas.industry_type import (

    IndustryTypeCreate,

    IndustryTypeUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["IndustryTypeService"]





class IndustryTypeService:

    def __init__(self, repository: Optional[IndustryTypeRepository] = None) -> None:

        self.repository = repository or IndustryTypeRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> IndustryType:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Industry Type", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: IndustryType

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> IndustryType:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[IndustryType]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[IndustryType].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:industry'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: IndustryTypeCreate

    ) -> IndustryType:

        row = IndustryType(

            business_id=business_id,

            name=payload.industry,

            industry=payload.industry,

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

        payload: IndustryTypeUpdate,

    ) -> IndustryType:

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

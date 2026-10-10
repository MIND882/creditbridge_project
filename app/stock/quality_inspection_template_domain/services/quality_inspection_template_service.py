"""Business logic for Quality Inspection Template -- port of

``erpnext/stock/doctype/quality_inspection_template/quality_inspection_template.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.quality_inspection_template_domain.models.quality_inspection_template import QualityInspectionTemplate

from app.stock.quality_inspection_template_domain.repositories.quality_inspection_template_repository import (

    QualityInspectionTemplateRepository,

)

from app.stock.quality_inspection_template_domain.schemas.quality_inspection_template import (

    QualityInspectionTemplateCreate,

    QualityInspectionTemplateUpdate,

)

from app.stock.item_quality_inspection_parameter_domain.models.item_quality_inspection_parameter import ItemQualityInspectionParameter

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["QualityInspectionTemplateService"]





class QualityInspectionTemplateService:

    def __init__(self, repository: Optional[QualityInspectionTemplateRepository] = None) -> None:

        self.repository = repository or QualityInspectionTemplateRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> QualityInspectionTemplate:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Quality Inspection Template", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: QualityInspectionTemplate

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> QualityInspectionTemplate:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[QualityInspectionTemplate]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[QualityInspectionTemplate].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:quality_inspection_template_name'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: QualityInspectionTemplateCreate

    ) -> QualityInspectionTemplate:

        row = QualityInspectionTemplate(

            business_id=business_id,

            name=payload.quality_inspection_template_name,

            quality_inspection_template_name=payload.quality_inspection_template_name,

        )

        self._replace_item_quality_inspection_parameter(business_id, row, [x.model_dump() for x in payload.item_quality_inspection_parameter])



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

        payload: QualityInspectionTemplateUpdate,

    ) -> QualityInspectionTemplate:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "item_quality_inspection_parameter":

                    self._replace_item_quality_inspection_parameter(business_id, row, value or [])

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



    def _replace_item_quality_inspection_parameter(

        self, business_id: uuid.UUID, row: QualityInspectionTemplate, item_quality_inspection_parameter: list[dict]

    ) -> None:

        row.item_quality_inspection_parameter.clear()

        for idx, entry in enumerate(item_quality_inspection_parameter, start=1):

            row.item_quality_inspection_parameter.append(

                ItemQualityInspectionParameter(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )

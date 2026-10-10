"""Business logic for Quality Inspection -- port of

``erpnext/stock/doctype/quality_inspection/quality_inspection.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 7 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.quality_inspection_domain.models.quality_inspection import QualityInspection

from app.stock.quality_inspection_domain.repositories.quality_inspection_repository import (

    QualityInspectionRepository,

)

from app.stock.quality_inspection_domain.schemas.quality_inspection import (

    QualityInspectionCreate,

    QualityInspectionUpdate,

)

from app.stock.quality_inspection_reading_domain.models.quality_inspection_reading import QualityInspectionReading

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["QualityInspectionService"]





class QualityInspectionService:

    def __init__(self, repository: Optional[QualityInspectionRepository] = None) -> None:

        self.repository = repository or QualityInspectionRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> QualityInspection:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Quality Inspection", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: QualityInspection

    ) -> None:

        """

        Upstream has 7 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> QualityInspection:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[QualityInspection]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[QualityInspection].build(

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

                select(func.count()).select_from(QualityInspection).where(

                    QualityInspection.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: QualityInspectionCreate

    ) -> QualityInspection:

        row = QualityInspection(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            report_date=payload.report_date,

            inspection_type=payload.inspection_type,

            reference_type=payload.reference_type,

            reference_name=payload.reference_name,

            item_code_id=payload.item_code_id,

            item_serial_no_id=payload.item_serial_no_id,

            batch_no_id=payload.batch_no_id,

            sample_size=payload.sample_size,

            item_name=payload.item_name,

            description=payload.description,

            inspected_by=payload.inspected_by,

            verified_by=payload.verified_by,

            bom_no=payload.bom_no,

            remarks=payload.remarks,

            amended_from_id=payload.amended_from_id,

            quality_inspection_template_id=payload.quality_inspection_template_id,

            status=payload.status,

            manual_inspection=payload.manual_inspection,

            child_row_reference=payload.child_row_reference,

            company=payload.company,

            letter_head=payload.letter_head,

        )

        self._replace_readings(business_id, row, [x.model_dump() for x in payload.readings])



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

        payload: QualityInspectionUpdate,

    ) -> QualityInspection:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "readings":

                    self._replace_readings(business_id, row, value or [])

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> QualityInspection:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Quality Inspection")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> QualityInspection:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Quality Inspection")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_readings(

        self, business_id: uuid.UUID, row: QualityInspection, readings: list[dict]

    ) -> None:

        row.readings.clear()

        for idx, entry in enumerate(readings, start=1):

            row.readings.append(

                QualityInspectionReading(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )

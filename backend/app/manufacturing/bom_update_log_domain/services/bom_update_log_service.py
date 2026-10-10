"""Business logic for BOM Update Log -- port of

``erpnext/manufacturing/doctype/bom_update_log/bom_update_log.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_update_log_domain.models.bom_update_log import BomUpdateLog

from app.manufacturing.bom_update_log_domain.repositories.bom_update_log_repository import (

    BomUpdateLogRepository,

)

from app.manufacturing.bom_update_log_domain.schemas.bom_update_log import (

    BomUpdateLogCreate,

    BomUpdateLogUpdate,

)

from app.manufacturing.bom_update_batch_domain.models.bom_update_batch import BomUpdateBatch

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["BomUpdateLogService"]





class BomUpdateLogService:

    def __init__(self, repository: Optional[BomUpdateLogRepository] = None) -> None:

        self.repository = repository or BomUpdateLogRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomUpdateLog:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BOM Update Log", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: BomUpdateLog

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomUpdateLog:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BomUpdateLog]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BomUpdateLog].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``pattern:BOM-UPDT-LOG-``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(BomUpdateLog).where(

                    BomUpdateLog.business_id == business_id

                )

            )

            or 0

        )

        return f"pattern:BOM-UPDT-LOG-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BomUpdateLogCreate

    ) -> BomUpdateLog:

        row = BomUpdateLog(

            business_id=business_id,

            name=self.next_name(db, business_id),

            update_type=payload.update_type,

            status=payload.status,

            current_bom_id=payload.current_bom_id,

            new_bom_id=payload.new_bom_id,

            error_log=payload.error_log,

            current_level=payload.current_level,

            processed_boms=payload.processed_boms,

            amended_from_id=payload.amended_from_id,

        )

        self._replace_bom_batches(business_id, row, [x.model_dump() for x in payload.bom_batches])



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

        payload: BomUpdateLogUpdate,

    ) -> BomUpdateLog:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "bom_batches":

                    self._replace_bom_batches(business_id, row, value or [])

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

    ) -> BomUpdateLog:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "BOM Update Log")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomUpdateLog:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "BOM Update Log")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_bom_batches(

        self, business_id: uuid.UUID, row: BomUpdateLog, bom_batches: list[dict]

    ) -> None:

        row.bom_batches.clear()

        for idx, entry in enumerate(bom_batches, start=1):

            row.bom_batches.append(

                BomUpdateBatch(

                    business_id=business_id,

                    idx=idx,

                    parenttype="BOM Update Log",

                    parentfield="bom_batches",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )

"""Business logic for Operation -- port of

``erpnext/manufacturing/doctype/operation/operation.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.operation_domain.models.operation import Operation

from app.manufacturing.operation_domain.repositories.operation_repository import (

    OperationRepository,

)

from app.manufacturing.operation_domain.schemas.operation import (

    OperationCreate,

    OperationUpdate,

)

from app.manufacturing.sub_operation_domain.models.sub_operation import SubOperation

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["OperationService"]





class OperationService:

    def __init__(self, repository: Optional[OperationRepository] = None) -> None:

        self.repository = repository or OperationRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Operation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Operation", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Operation

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Operation:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Operation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Operation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``prompt``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(Operation).where(

                    Operation.business_id == business_id

                )

            )

            or 0

        )

        return f"prompt{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: OperationCreate

    ) -> Operation:

        row = Operation(

            business_id=business_id,

            name=self.next_name(db, business_id),

            workstation_id=payload.workstation_id,

            is_corrective_operation=payload.is_corrective_operation,

            create_job_card_based_on_batch_size=payload.create_job_card_based_on_batch_size,

            quality_inspection_template_id=payload.quality_inspection_template_id,

            batch_size=payload.batch_size,

            total_operation_time=payload.total_operation_time,

            description=payload.description,

            work_instruction=payload.work_instruction,

        )

        self._replace_sub_operations(business_id, row, [x.model_dump() for x in payload.sub_operations])



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

        payload: OperationUpdate,

    ) -> Operation:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "sub_operations":

                    self._replace_sub_operations(business_id, row, value or [])

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



    def _replace_sub_operations(

        self, business_id: uuid.UUID, row: Operation, sub_operations: list[dict]

    ) -> None:

        row.sub_operations.clear()

        for idx, entry in enumerate(sub_operations, start=1):

            row.sub_operations.append(

                SubOperation(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Operation",

                    parentfield="sub_operations",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )

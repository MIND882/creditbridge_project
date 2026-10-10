# HAND-WRITTEN

"""

Business logic for Process Deferred Accounting -- port of

``erpnext/accounts/doctype/process_deferred_accounting/process_deferred_accounting.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    on_submit

    on_cancel



**Upstream has 1 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_deferred_accounting_domain.models.process_deferred_accounting import ProcessDeferredAccounting

from app.accounts.process_deferred_accounting_domain.repositories.process_deferred_accounting_repository import (

    ProcessDeferredAccountingRepository,

)

from app.accounts.process_deferred_accounting_domain.schemas.process_deferred_accounting import (

    ProcessDeferredAccountingCreate,

    ProcessDeferredAccountingUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProcessDeferredAccountingService"]





class ProcessDeferredAccountingService:

    def __init__(self, repository: Optional[ProcessDeferredAccountingRepository] = None) -> None:

        self.repository = repository or ProcessDeferredAccountingRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessDeferredAccounting:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Process Deferred Accounting", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ProcessDeferredAccounting

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **1 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessDeferredAccounting:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProcessDeferredAccounting]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProcessDeferredAccounting].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ProcessDeferredAccounting).where(

                    ProcessDeferredAccounting.business_id == business_id

                )

            )

            or 0

        )

        return f"PRO-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ProcessDeferredAccountingCreate

    ) -> ProcessDeferredAccounting:

        row = ProcessDeferredAccounting(

            business_id=business_id,

            name=self.next_name(db, business_id),

            type=payload.type,

            amended_from=payload.amended_from,

            start_date=payload.start_date,

            end_date=payload.end_date,

            posting_date=payload.posting_date,

            account_id=payload.account_id,

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

        payload: ProcessDeferredAccountingUpdate,

    ) -> ProcessDeferredAccounting:

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessDeferredAccounting:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Process Deferred Accounting")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessDeferredAccounting:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Process Deferred Accounting")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

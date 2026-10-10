# HAND-WRITTEN

"""

Business logic for Process Payment Reconciliation Log -- port of

``erpnext/accounts/doctype/process_payment_reconciliation_log/process_payment_reconciliation_log.py``.







Upstream hooks:

    (none -- upstream's controller defines no hooks)



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_payment_reconciliation_log_domain.models.process_payment_reconciliation_log import ProcessPaymentReconciliationLog

from app.accounts.process_payment_reconciliation_log_allocations_domain.models.process_payment_reconciliation_log_allocations import ProcessPaymentReconciliationLogAllocations

from app.accounts.process_payment_reconciliation_log_domain.repositories.process_payment_reconciliation_log_repository import (

    ProcessPaymentReconciliationLogRepository,

)

from app.accounts.process_payment_reconciliation_log_domain.schemas.process_payment_reconciliation_log import (

    ProcessPaymentReconciliationLogCreate,

    ProcessPaymentReconciliationLogUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProcessPaymentReconciliationLogService"]





class ProcessPaymentReconciliationLogService:

    def __init__(self, repository: Optional[ProcessPaymentReconciliationLogRepository] = None) -> None:

        self.repository = repository or ProcessPaymentReconciliationLogRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessPaymentReconciliationLog:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Process Payment Reconciliation Log", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ProcessPaymentReconciliationLog

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessPaymentReconciliationLog:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProcessPaymentReconciliationLog]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProcessPaymentReconciliationLog].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_allocations(

        self, business_id: uuid.UUID, row: ProcessPaymentReconciliationLog, items: list[dict]

    ) -> None:

        row.allocations.clear()

        for idx, item in enumerate(items, start=1):

            row.allocations.append(

                ProcessPaymentReconciliationLogAllocations(

                    business_id=business_id,

                    idx=idx,

                    reference_type=item.get('reference_type'),

                    reference_name=item.get('reference_name'),

                    reference_row=item.get('reference_row'),

                    invoice_type=item.get('invoice_type'),

                    invoice_number=item.get('invoice_number'),

                    allocated_amount=item.get('allocated_amount'),

                    unreconciled_amount=item.get('unreconciled_amount'),

                    amount=item.get('amount'),

                    is_advance=item.get('is_advance'),

                    difference_amount=item.get('difference_amount'),

                    difference_account_id=item.get('difference_account_id'),

                    exchange_rate=item.get('exchange_rate'),

                    currency=item.get('currency'),

                    reconciled=item.get('reconciled'),

                    gain_loss_posting_date=item.get('gain_loss_posting_date'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ProcessPaymentReconciliationLog).where(

                    ProcessPaymentReconciliationLog.business_id == business_id

                )

            )

            or 0

        )

        return f"PRO-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ProcessPaymentReconciliationLogCreate

    ) -> ProcessPaymentReconciliationLog:

        row = ProcessPaymentReconciliationLog(

            business_id=business_id,

            name=self.next_name(db, business_id),

            reconciled=payload.reconciled,

            total_allocations=payload.total_allocations,

            allocated=payload.allocated,

            reconciled_entries=payload.reconciled_entries,

            error_log=payload.error_log,

            process_pr=payload.process_pr,

            status=payload.status,

        )

        self._replace_allocations(business_id, row, [x.model_dump() for x in payload.allocations])



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

        payload: ProcessPaymentReconciliationLogUpdate,

    ) -> ProcessPaymentReconciliationLog:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "allocations":

                    self._replace_allocations(business_id, row, value or [])

                else:

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

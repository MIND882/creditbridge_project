# HAND-WRITTEN

"""

Business logic for Process Payment Reconciliation -- port of

``erpnext/accounts/doctype/process_payment_reconciliation/process_payment_reconciliation.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    on_discard

    validate

    validate_receivable_payable_account

    validate_bank_cash_account

    before_save

    on_submit

    on_cancel



**Upstream has 3 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_payment_reconciliation_domain.models.process_payment_reconciliation import ProcessPaymentReconciliation

from app.accounts.process_payment_reconciliation_domain.repositories.process_payment_reconciliation_repository import (

    ProcessPaymentReconciliationRepository,

)

from app.accounts.process_payment_reconciliation_domain.schemas.process_payment_reconciliation import (

    ProcessPaymentReconciliationCreate,

    ProcessPaymentReconciliationUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProcessPaymentReconciliationService"]





class ProcessPaymentReconciliationService:

    def __init__(self, repository: Optional[ProcessPaymentReconciliationRepository] = None) -> None:

        self.repository = repository or ProcessPaymentReconciliationRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessPaymentReconciliation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Process Payment Reconciliation", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ProcessPaymentReconciliation

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **3 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessPaymentReconciliation:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProcessPaymentReconciliation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProcessPaymentReconciliation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ProcessPaymentReconciliation).where(

                    ProcessPaymentReconciliation.business_id == business_id

                )

            )

            or 0

        )

        return f"PRO-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ProcessPaymentReconciliationCreate

    ) -> ProcessPaymentReconciliation:

        row = ProcessPaymentReconciliation(

            business_id=business_id,

            name=self.next_name(db, business_id),

            status=payload.status,

            party_type=payload.party_type,

            party=payload.party,

            receivable_payable_account_id=payload.receivable_payable_account_id,

            from_invoice_date=payload.from_invoice_date,

            to_invoice_date=payload.to_invoice_date,

            from_payment_date=payload.from_payment_date,

            to_payment_date=payload.to_payment_date,

            cost_center_id=payload.cost_center_id,

            bank_cash_account_id=payload.bank_cash_account_id,

            error_log=payload.error_log,

            amended_from=payload.amended_from,

            default_advance_account_id=payload.default_advance_account_id,

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

        payload: ProcessPaymentReconciliationUpdate,

    ) -> ProcessPaymentReconciliation:

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

    ) -> ProcessPaymentReconciliation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Process Payment Reconciliation")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessPaymentReconciliation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Process Payment Reconciliation")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

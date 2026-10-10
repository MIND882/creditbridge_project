# HAND-WRITTEN

"""

Business logic for Unreconcile Payment -- port of

``erpnext/accounts/doctype/unreconcile_payment/unreconcile_payment.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    get_allocations_from_payment

    add_references

    on_submit



**Upstream has 1 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.unreconcile_payment_domain.models.unreconcile_payment import UnreconcilePayment

from app.accounts.process_payment_reconciliation_log_allocations_domain.models.process_payment_reconciliation_log_allocations import ProcessPaymentReconciliationLogAllocations

from app.accounts.unreconcile_payment_domain.repositories.unreconcile_payment_repository import (

    UnreconcilePaymentRepository,

)

from app.accounts.unreconcile_payment_domain.schemas.unreconcile_payment import (

    UnreconcilePaymentCreate,

    UnreconcilePaymentUpdate,

)

from app.accounts.unreconcile_payment_entries_domain.models.unreconcile_payment_entries import UnreconcilePaymentEntries  # noqa: F401

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["UnreconcilePaymentService"]





class UnreconcilePaymentService:

    def __init__(self, repository: Optional[UnreconcilePaymentRepository] = None) -> None:

        self.repository = repository or UnreconcilePaymentRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> UnreconcilePayment:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Unreconcile Payment", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: UnreconcilePayment

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

    ) -> UnreconcilePayment:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[UnreconcilePayment]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[UnreconcilePayment].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_allocations(

        self, business_id: uuid.UUID, row: UnreconcilePayment, items: list[dict]

    ) -> None:

        row.allocations.clear()

        for idx, item in enumerate(items, start=1):

            row.allocations.append(

                UnreconcilePaymentEntries(

                    business_id=business_id,

                    idx=idx,

                    reference_name=item.get('reference_name'),

                    allocated_amount=item.get('allocated_amount'),

                    unlinked=item.get('unlinked'),

                    reference_doctype=item.get('reference_doctype'),

                    account=item.get('account'),

                    party_type=item.get('party_type'),

                    party=item.get('party'),

                    account_currency=item.get('account_currency'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(UnreconcilePayment).where(

                    UnreconcilePayment.business_id == business_id

                )

            )

            or 0

        )

        return f"UNR-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: UnreconcilePaymentCreate

    ) -> UnreconcilePayment:

        row = UnreconcilePayment(

            business_id=business_id,

            name=self.next_name(db, business_id),

            amended_from=payload.amended_from,

            voucher_type=payload.voucher_type,

            voucher_no=payload.voucher_no,

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

        payload: UnreconcilePaymentUpdate,

    ) -> UnreconcilePayment:

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> UnreconcilePayment:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Unreconcile Payment")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> UnreconcilePayment:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Unreconcile Payment")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

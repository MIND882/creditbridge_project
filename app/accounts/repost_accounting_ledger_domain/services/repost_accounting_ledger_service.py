# HAND-WRITTEN

"""

Business logic for Repost Accounting Ledger -- port of

``erpnext/accounts/doctype/repost_accounting_ledger/repost_accounting_ledger.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    validate_repost_preconditions

    validate_for_deferred_accounting

    validate_for_closed_fiscal_year

    validate_vouchers

    validate_no_duplicate_vouchers

    validate_vouchers_are_submitted

    on_discard

    get_existing_ledger_entries

    generate_preview_data

    generate_preview

    on_submit

    before_cancel

    on_cancel

    start_repost



**Upstream has 10 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.repost_accounting_ledger_domain.models.repost_accounting_ledger import RepostAccountingLedger

from app.accounts.repost_accounting_ledger_items_domain.models.repost_accounting_ledger_items import RepostAccountingLedgerItems

from app.accounts.repost_accounting_ledger_domain.repositories.repost_accounting_ledger_repository import (

    RepostAccountingLedgerRepository,

)

from app.accounts.repost_accounting_ledger_domain.schemas.repost_accounting_ledger import (

    RepostAccountingLedgerCreate,

    RepostAccountingLedgerUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["RepostAccountingLedgerService"]





class RepostAccountingLedgerService:

    def __init__(self, repository: Optional[RepostAccountingLedgerRepository] = None) -> None:

        self.repository = repository or RepostAccountingLedgerRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostAccountingLedger:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Repost Accounting Ledger", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: RepostAccountingLedger

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **10 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostAccountingLedger:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[RepostAccountingLedger]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[RepostAccountingLedger].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_vouchers(

        self, business_id: uuid.UUID, row: RepostAccountingLedger, items: list[dict]

    ) -> None:

        row.vouchers.clear()

        for idx, item in enumerate(items, start=1):

            row.vouchers.append(

                RepostAccountingLedgerItems(

                    business_id=business_id,

                    idx=idx,

                    voucher_type=item.get('voucher_type'),

                    voucher_no=item.get('voucher_no'),

                    status=item.get('status'),

                    traceback=item.get('traceback'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(RepostAccountingLedger).where(

                    RepostAccountingLedger.business_id == business_id

                )

            )

            or 0

        )

        return f"REP-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: RepostAccountingLedgerCreate

    ) -> RepostAccountingLedger:

        row = RepostAccountingLedger(

            business_id=business_id,

            name=self.next_name(db, business_id),

            amended_from=payload.amended_from,

            delete_cancelled_entries=payload.delete_cancelled_entries,

            error_log=payload.error_log,

            status=payload.status,

            scheduled_job=payload.scheduled_job,

        )

        self._replace_vouchers(business_id, row, [x.model_dump() for x in payload.vouchers])



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

        payload: RepostAccountingLedgerUpdate,

    ) -> RepostAccountingLedger:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "vouchers":

                    self._replace_vouchers(business_id, row, value or [])

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

    ) -> RepostAccountingLedger:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Repost Accounting Ledger")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostAccountingLedger:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Repost Accounting Ledger")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

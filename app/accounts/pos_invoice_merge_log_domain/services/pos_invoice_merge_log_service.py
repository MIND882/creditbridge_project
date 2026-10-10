# HAND-WRITTEN

"""

Business logic for POS Invoice Merge Log -- port of

``erpnext/accounts/doctype/pos_invoice_merge_log/pos_invoice_merge_log.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    validate_duplicate_pos_invoices

    validate_customer

    validate_pos_invoice_status

    on_submit

    on_cancel

    process_merging_into_sales_invoice

    process_merging_into_credit_notes

    distinguish_return_pos_invoices

    merge_pos_invoice_into

    get_new_sales_invoice

    update_pos_invoices

    serial_and_batch_bundle_reference_for_pos_invoice

    delink_serial_and_batch_bundle

    get_serial_and_batch_bundles

    cancel_linked_invoices



**Upstream has 7 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_invoice_merge_log_domain.models.pos_invoice_merge_log import POSInvoiceMergeLog

from app.accounts.pos_invoice_reference_domain.models.pos_invoice_reference import POSInvoiceReference

from app.accounts.pos_invoice_merge_log_domain.repositories.pos_invoice_merge_log_repository import (

    POSInvoiceMergeLogRepository,

)

from app.accounts.pos_invoice_merge_log_domain.schemas.pos_invoice_merge_log import (

    POSInvoiceMergeLogCreate,

    POSInvoiceMergeLogUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSInvoiceMergeLogService"]





class POSInvoiceMergeLogService:

    def __init__(self, repository: Optional[POSInvoiceMergeLogRepository] = None) -> None:

        self.repository = repository or POSInvoiceMergeLogRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSInvoiceMergeLog:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Invoice Merge Log", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: POSInvoiceMergeLog

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **7 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSInvoiceMergeLog:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSInvoiceMergeLog]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSInvoiceMergeLog].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_pos_invoices(

        self, business_id: uuid.UUID, row: POSInvoiceMergeLog, items: list[dict]

    ) -> None:

        row.pos_invoices.clear()

        for idx, item in enumerate(items, start=1):

            row.pos_invoices.append(

                POSInvoiceReference(

                    business_id=business_id,

                    idx=idx,

                    parenttype='POS Invoice Merge Log',

                    pos_invoice=item.get('pos_invoice'),

                    customer=item.get('customer'),

                    posting_date=item.get('posting_date'),

                    grand_total=item.get('grand_total'),

                    is_return=item.get('is_return'),

                    return_against=item.get('return_against'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(POSInvoiceMergeLog).where(

                    POSInvoiceMergeLog.business_id == business_id

                )

            )

            or 0

        )

        return f"POS-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: POSInvoiceMergeLogCreate

    ) -> POSInvoiceMergeLog:

        row = POSInvoiceMergeLog(

            business_id=business_id,

            name=self.next_name(db, business_id),

            posting_date=payload.posting_date,

            customer=payload.customer,

            amended_from=payload.amended_from,

            consolidated_invoice=payload.consolidated_invoice,

            consolidated_credit_note=payload.consolidated_credit_note,

            pos_closing_entry=payload.pos_closing_entry,

            merge_invoices_based_on=payload.merge_invoices_based_on,

            customer_group=payload.customer_group,

            posting_time=payload.posting_time,

        )

        self._replace_pos_invoices(business_id, row, [x.model_dump() for x in payload.pos_invoices])



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

        payload: POSInvoiceMergeLogUpdate,

    ) -> POSInvoiceMergeLog:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "pos_invoices":

                    self._replace_pos_invoices(business_id, row, value or [])

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

    ) -> POSInvoiceMergeLog:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "POS Invoice Merge Log")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSInvoiceMergeLog:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "POS Invoice Merge Log")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

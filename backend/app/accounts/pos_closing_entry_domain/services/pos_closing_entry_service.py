# HAND-WRITTEN

"""

Business logic for POS Closing Entry -- port of

``erpnext/accounts/doctype/pos_closing_entry/pos_closing_entry.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    set_posting_date_and_time

    fetch_invoice_type

    validate_pos_opening_entry

    validate_invoice_mode

    validate_duplicate_pos_invoices

    validate_pos_invoices

    validate_duplicate_sales_invoices

    validate_sales_invoices

    on_submit

    before_cancel

    on_cancel

    retry

    update_opening_entry

    update_sales_invoices_closing_entry

    check_pce_is_cancellable



**Upstream has 7 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_closing_entry_domain.models.pos_closing_entry import POSClosingEntry

from app.accounts.pos_closing_entry_detail_domain.models.pos_closing_entry_detail import POSClosingEntryDetail

from app.accounts.pos_closing_entry_taxes_domain.models.pos_closing_entry_taxes import POSClosingEntryTaxes

from app.accounts.pos_invoice_reference_domain.models.pos_invoice_reference import POSInvoiceReference

from app.accounts.sales_invoice_reference_domain.models.sales_invoice_reference import SalesInvoiceReference

from app.accounts.pos_closing_entry_domain.repositories.pos_closing_entry_repository import (

    POSClosingEntryRepository,

)

from app.accounts.pos_closing_entry_domain.schemas.pos_closing_entry import (

    POSClosingEntryCreate,

    POSClosingEntryUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSClosingEntryService"]





class POSClosingEntryService:

    def __init__(self, repository: Optional[POSClosingEntryRepository] = None) -> None:

        self.repository = repository or POSClosingEntryRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSClosingEntry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Closing Entry", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: POSClosingEntry

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

    ) -> POSClosingEntry:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSClosingEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSClosingEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_payment_reconciliation(

        self, business_id: uuid.UUID, row: POSClosingEntry, items: list[dict]

    ) -> None:

        row.payment_reconciliation.clear()

        for idx, item in enumerate(items, start=1):

            row.payment_reconciliation.append(

                POSClosingEntryDetail(

                    business_id=business_id,

                    idx=idx,

                    mode_of_payment_id=item.get('mode_of_payment_id'),

                    expected_amount=item.get('expected_amount'),

                    difference=item.get('difference'),

                    opening_amount=item.get('opening_amount'),

                    closing_amount=item.get('closing_amount'),

                )

            )



    def _replace_taxes(

        self, business_id: uuid.UUID, row: POSClosingEntry, items: list[dict]

    ) -> None:

        row.taxes.clear()

        for idx, item in enumerate(items, start=1):

            row.taxes.append(

                POSClosingEntryTaxes(

                    business_id=business_id,

                    idx=idx,

                    amount=item.get('amount'),

                    account_head_id=item.get('account_head_id'),

                )

            )



    def _replace_pos_invoices(

        self, business_id: uuid.UUID, row: POSClosingEntry, items: list[dict]

    ) -> None:

        row.pos_invoices.clear()

        for idx, item in enumerate(items, start=1):

            row.pos_invoices.append(

                POSInvoiceReference(

                    business_id=business_id,

                    idx=idx,

                    parenttype='POS Closing Entry',

                    pos_invoice=item.get('pos_invoice'),

                    customer=item.get('customer'),

                    posting_date=item.get('posting_date'),

                    grand_total=item.get('grand_total'),

                    is_return=item.get('is_return'),

                    return_against=item.get('return_against'),

                )

            )



    def _replace_sales_invoices(

        self, business_id: uuid.UUID, row: POSClosingEntry, items: list[dict]

    ) -> None:

        row.sales_invoices.clear()

        for idx, item in enumerate(items, start=1):

            row.sales_invoices.append(

                SalesInvoiceReference(

                    business_id=business_id,

                    idx=idx,

                    sales_invoice=item.get('sales_invoice'),

                    posting_date=item.get('posting_date'),

                    customer=item.get('customer'),

                    is_return=item.get('is_return'),

                    return_against=item.get('return_against'),

                    grand_total=item.get('grand_total'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(POSClosingEntry).where(

                    POSClosingEntry.business_id == business_id

                )

            )

            or 0

        )

        return f"POS-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: POSClosingEntryCreate

    ) -> POSClosingEntry:

        row = POSClosingEntry(

            business_id=business_id,

            name=self.next_name(db, business_id),

            period_start_date=payload.period_start_date,

            period_end_date=payload.period_end_date,

            posting_date=payload.posting_date,

            pos_profile=payload.pos_profile,

            user=payload.user,

            grand_total=payload.grand_total,

            net_total=payload.net_total,

            total_quantity=payload.total_quantity,

            amended_from=payload.amended_from,

            pos_opening_entry=payload.pos_opening_entry,

            status=payload.status,

            error_message=payload.error_message,

            posting_time=payload.posting_time,

            total_taxes_and_charges=payload.total_taxes_and_charges,

        )

        self._replace_payment_reconciliation(business_id, row, [x.model_dump() for x in payload.payment_reconciliation])

        self._replace_taxes(business_id, row, [x.model_dump() for x in payload.taxes])

        self._replace_pos_invoices(business_id, row, [x.model_dump() for x in payload.pos_invoices])

        self._replace_sales_invoices(business_id, row, [x.model_dump() for x in payload.sales_invoices])



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

        payload: POSClosingEntryUpdate,

    ) -> POSClosingEntry:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "payment_reconciliation":

                    self._replace_payment_reconciliation(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "taxes":

                    self._replace_taxes(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "pos_invoices":

                    self._replace_pos_invoices(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "sales_invoices":

                    self._replace_sales_invoices(business_id, row, value or [])

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

    ) -> POSClosingEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "POS Closing Entry")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSClosingEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "POS Closing Entry")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

# HAND-WRITTEN

"""

Business logic for Invoice Discounting -- port of

``erpnext/accounts/doctype/invoice_discounting/invoice_discounting.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    set_end_date

    validate_mandatory

    validate_invoices

    calculate_total_amount

    on_submit

    on_cancel

    set_status

    update_sales_invoice

    make_gl_entries

    create_disbursement_entry

    close_loan



**Upstream has 3 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.invoice_discounting_domain.models.invoice_discounting import InvoiceDiscounting

from app.accounts.discounted_invoice_domain.models.discounted_invoice import DiscountedInvoice

from app.accounts.invoice_discounting_domain.repositories.invoice_discounting_repository import (

    InvoiceDiscountingRepository,

)

from app.accounts.invoice_discounting_domain.schemas.invoice_discounting import (

    InvoiceDiscountingCreate,

    InvoiceDiscountingUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["InvoiceDiscountingService"]





class InvoiceDiscountingService:

    def __init__(self, repository: Optional[InvoiceDiscountingRepository] = None) -> None:

        self.repository = repository or InvoiceDiscountingRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> InvoiceDiscounting:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Invoice Discounting", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: InvoiceDiscounting

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

    ) -> InvoiceDiscounting:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[InvoiceDiscounting]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[InvoiceDiscounting].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_invoices(

        self, business_id: uuid.UUID, row: InvoiceDiscounting, items: list[dict]

    ) -> None:

        row.invoices.clear()

        for idx, item in enumerate(items, start=1):

            row.invoices.append(

                DiscountedInvoice(

                    business_id=business_id,

                    idx=idx,

                    sales_invoice=item.get('sales_invoice'),

                    customer=item.get('customer'),

                    posting_date=item.get('posting_date'),

                    outstanding_amount=item.get('outstanding_amount'),

                    debit_to_id=item.get('debit_to_id'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(InvoiceDiscounting).where(

                    InvoiceDiscounting.business_id == business_id

                )

            )

            or 0

        )

        return f"INV-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: InvoiceDiscountingCreate

    ) -> InvoiceDiscounting:

        row = InvoiceDiscounting(

            business_id=business_id,

            name=self.next_name(db, business_id),

            posting_date=payload.posting_date,

            loan_start_date=payload.loan_start_date,

            loan_period=payload.loan_period,

            loan_end_date=payload.loan_end_date,

            status=payload.status,

            total_amount=payload.total_amount,

            bank_charges=payload.bank_charges,

            short_term_loan_id=payload.short_term_loan_id,

            bank_account_id=payload.bank_account_id,

            bank_charges_account_id=payload.bank_charges_account_id,

            accounts_receivable_credit_id=payload.accounts_receivable_credit_id,

            accounts_receivable_discounted_id=payload.accounts_receivable_discounted_id,

            accounts_receivable_unpaid_id=payload.accounts_receivable_unpaid_id,

            amended_from=payload.amended_from,

        )

        self._replace_invoices(business_id, row, [x.model_dump() for x in payload.invoices])



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

        payload: InvoiceDiscountingUpdate,

    ) -> InvoiceDiscounting:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "invoices":

                    self._replace_invoices(business_id, row, value or [])

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

    ) -> InvoiceDiscounting:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Invoice Discounting")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> InvoiceDiscounting:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Invoice Discounting")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

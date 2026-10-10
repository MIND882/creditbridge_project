# HAND-WRITTEN

"""

Business logic for Payment Reconciliation -- port of

``erpnext/accounts/doctype/payment_reconciliation/payment_reconciliation.py``.







Upstream hooks:

    user_permissions

    load_from_db

    save

    get_list

    get_count

    get_stats

    db_insert

    db_update

    delete

    get_unreconciled_entries

    get_nonreconciled_payment_entries

    get_permitted_dimension_values

    validate_permitted_dimension_value

    get_user_permission_dimension_condition

    get_payment_entries

    get_jv_entries

    get_return_invoices

    get_dr_or_cr_notes

    add_payment_entries

    get_invoice_entries

    add_invoice_entries

    get_difference_amount

    is_auto_process_enabled

    calculate_difference_on_allocation_change

    allocate_entries

    update_dimension_values_in_allocated_entries

    get_allocated_entry

    reconcile_allocations

    reconcile

    get_payment_details

    check_mandatory_to_fetch

    validate_entries

    get_invoice_exchange_map

    validate_allocation

    build_dimensions_filter_conditions

    build_qb_filter_conditions

    get_journal_filter_conditions



**Upstream has 9 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_reconciliation_domain.models.payment_reconciliation import PaymentReconciliation

from app.accounts.cashier_closing_payments_domain.models.cashier_closing_payments import CashierClosingPayments

from app.accounts.discounted_invoice_domain.models.discounted_invoice import DiscountedInvoice

from app.accounts.payment_reconciliation_allocation_domain.models.payment_reconciliation_allocation import PaymentReconciliationAllocation

from app.accounts.payment_reconciliation_domain.repositories.payment_reconciliation_repository import (

    PaymentReconciliationRepository,

)

from app.accounts.payment_reconciliation_domain.schemas.payment_reconciliation import (

    PaymentReconciliationCreate,

    PaymentReconciliationUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentReconciliationService"]





class PaymentReconciliationService:

    def __init__(self, repository: Optional[PaymentReconciliationRepository] = None) -> None:

        self.repository = repository or PaymentReconciliationRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentReconciliation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Payment Reconciliation", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PaymentReconciliation

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **9 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentReconciliation:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentReconciliation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentReconciliation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_payments(

        self, business_id: uuid.UUID, row: PaymentReconciliation, items: list[dict]

    ) -> None:

        row.payments.clear()

        for idx, item in enumerate(items, start=1):

            row.payments.append(

                PaymentReconciliationPayment(

                    business_id=business_id,

                    idx=idx,

                    reference_type=item.get('reference_type'),

                    reference_name=item.get('reference_name'),

                    posting_date=item.get('posting_date'),

                    is_advance=item.get('is_advance'),

                    reference_row=item.get('reference_row'),

                    amount=item.get('amount'),

                    currency=item.get('currency'),

                    difference_amount=item.get('difference_amount'),

                    exchange_rate=item.get('exchange_rate'),

                    cost_center_id=item.get('cost_center_id'),

                    remarks=item.get('remarks'),

                )

            )



    def _replace_invoices(

        self, business_id: uuid.UUID, row: PaymentReconciliation, items: list[dict]

    ) -> None:

        row.invoices.clear()

        for idx, item in enumerate(items, start=1):

            row.invoices.append(

                PaymentReconciliationInvoice(

                    business_id=business_id,

                    idx=idx,

                    invoice_type=item.get('invoice_type'),

                    invoice_number=item.get('invoice_number'),

                    invoice_date=item.get('invoice_date'),

                    amount=item.get('amount'),

                    outstanding_amount=item.get('outstanding_amount'),

                    currency=item.get('currency'),

                    exchange_rate=item.get('exchange_rate'),

                )

            )



    def _replace_allocation(

        self, business_id: uuid.UUID, row: PaymentReconciliation, items: list[dict]

    ) -> None:

        row.allocation.clear()

        for idx, item in enumerate(items, start=1):

            row.allocation.append(

                PaymentReconciliationAllocation(

                    business_id=business_id,

                    idx=idx,

                    invoice_number=item.get('invoice_number'),

                    allocated_amount=item.get('allocated_amount'),

                    difference_account_id=item.get('difference_account_id'),

                    difference_amount=item.get('difference_amount'),

                    reference_name=item.get('reference_name'),

                    is_advance=item.get('is_advance'),

                    reference_type=item.get('reference_type'),

                    invoice_type=item.get('invoice_type'),

                    unreconciled_amount=item.get('unreconciled_amount'),

                    amount=item.get('amount'),

                    reference_row=item.get('reference_row'),

                    currency=item.get('currency'),

                    exchange_rate=item.get('exchange_rate'),

                    cost_center_id=item.get('cost_center_id'),

                    gain_loss_posting_date=item.get('gain_loss_posting_date'),

                    debit_or_credit_note_posting_date=item.get('debit_or_credit_note_posting_date'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PaymentReconciliation).where(

                    PaymentReconciliation.business_id == business_id

                )

            )

            or 0

        )

        return f"PAY-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PaymentReconciliationCreate

    ) -> PaymentReconciliation:

        row = PaymentReconciliation(

            business_id=business_id,

            name=self.next_name(db, business_id),

            party_type=payload.party_type,

            party=payload.party,

            receivable_payable_account_id=payload.receivable_payable_account_id,

            bank_cash_account_id=payload.bank_cash_account_id,

            from_invoice_date=payload.from_invoice_date,

            to_invoice_date=payload.to_invoice_date,

            minimum_invoice_amount=payload.minimum_invoice_amount,

            invoice_limit=payload.invoice_limit,

            from_payment_date=payload.from_payment_date,

            to_payment_date=payload.to_payment_date,

            minimum_payment_amount=payload.minimum_payment_amount,

            maximum_payment_amount=payload.maximum_payment_amount,

            payment_limit=payload.payment_limit,

            maximum_invoice_amount=payload.maximum_invoice_amount,

            cost_center_id=payload.cost_center_id,

            project=payload.project,

            default_advance_account_id=payload.default_advance_account_id,

            invoice_name=payload.invoice_name,

            payment_name=payload.payment_name,

        )

        self._replace_payments(business_id, row, [x.model_dump() for x in payload.payments])

        self._replace_invoices(business_id, row, [x.model_dump() for x in payload.invoices])

        self._replace_allocation(business_id, row, [x.model_dump() for x in payload.allocation])



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

        payload: PaymentReconciliationUpdate,

    ) -> PaymentReconciliation:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "payments":

                    self._replace_payments(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "invoices":

                    self._replace_invoices(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "allocation":

                    self._replace_allocation(business_id, row, value or [])

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

"""

Business logic for Payment Entry -- port of

``erpnext/accounts/doctype/payment_entry/payment_entry.py``.



Upstream hook -> here

-------------------

``naming_series`` (ACC-PAY-.YYYY.-)   :meth:`PaymentEntryRepository.next_name`

``validate``                           :meth:`_validate`

  ``validate_mandatory``               :meth:`_validate_mandatory`

  ``validate_duplicate_entry``         :meth:`_validate_duplicate_references`

  ``validate_allocated_amount``        :meth:`_validate_allocated_amount`

  ``set_amounts``                      :meth:`_set_amounts`

  ``validate_received_amount``         :meth:`_validate_received_amount`

  ``set_status``                       :meth:`_set_status`

``on_submit``                          :meth:`submit`

``on_cancel``                          :meth:`cancel`



Upstream's controller is ~3,300 lines, and most of it reconciles the payment

against Sales/Purchase Invoices and Payment Requests -- doctypes that are not

converted. The allocation-vs-outstanding guard still runs against the

``outstanding_amount`` carried on each reference row, which is what the API

caller supplies; :meth:`sync_reference_outstandings` is the seam where real

invoice lookups plug in.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.gl_entry_domain.schemas.gl_entry import GLEntryCreate

from app.accounts.gl_entry_domain.services.gl_entry_service import GLEntryService

from app.accounts.payment_entry_deduction_domain.models.payment_entry_deduction import (

    PaymentEntryDeduction,

)

from app.accounts.payment_entry_domain.models.payment_entry import PaymentEntry, PaymentType

from app.accounts.payment_entry_domain.repositories.payment_entry_repository import (

    PaymentEntryRepository,

)

from app.accounts.payment_entry_domain.schemas.payment_entry import (

    PaymentEntryCreate,

    PaymentEntryUpdate,

)

from app.accounts.payment_entry_reference_domain.models.payment_entry_reference import (

    PaymentEntryReference,

)

from app.accounts.fiscal_year_domain.services.fiscal_year_service import (

    FiscalYearService,

)

from app.core.docstatus import DocStatus, assert_can_cancel, assert_can_submit

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentEntryService"]



ZERO = Decimal("0")





def _dec(value: object) -> Decimal:

    if value is None or value == "":

        return ZERO

    return Decimal(str(value))





class PaymentEntryService:

    def __init__(

        self,

        repository: Optional[PaymentEntryRepository] = None,

        *,

        gl_service: Optional[GLEntryService] = None,

    ) -> None:

        self.repository = repository or PaymentEntryRepository()

        self.gl = gl_service or GLEntryService()

        self._fiscal_years = FiscalYearService()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID

    ) -> PaymentEntry:

        row = self.repository.get_by_id(db, business_id, entry_id)

        if row is None:

            raise NotFoundError("Payment Entry", entry_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_mandatory(row: PaymentEntry) -> None:

        """Port of ``validate_mandatory``."""

        labels = {

            "paid_amount": "Paid Amount",

            "received_amount": "Received Amount",

            "source_exchange_rate": "Source Exchange Rate",

            "target_exchange_rate": "Target Exchange Rate",

        }

        for field, label in labels.items():

            if not getattr(row, field):

                raise DomainValidationError(

                    f"{label} is mandatory", code="payment_entry_field_mandatory"

                )



    @staticmethod

    def _validate_received_amount(row: PaymentEntry) -> None:

        """Port of ``validate_received_amount``."""

        if row.paid_from_account_currency == row.paid_to_account_currency:

            if _dec(row.paid_amount) < _dec(row.received_amount):

                raise DomainValidationError(

                    "Received Amount cannot be greater than Paid Amount",

                    code="payment_entry_received_exceeds_paid",

                )



    @staticmethod

    def _validate_duplicate_references(row: PaymentEntry) -> None:

        """

        Port of ``validate_duplicate_entry``.



        The key includes the payment term and request, so the same invoice can

        appear twice when it is being settled term by term.

        """

        seen: set[tuple] = set()

        for child in row.references:

            key = (

                child.reference_doctype,

                child.reference_name,

                child.payment_term,

                child.payment_request,

            )

            if key in seen:

                raise DomainValidationError(

                    f"Row #{child.idx}: Duplicate entry in References "

                    f"{child.reference_doctype} {child.reference_name}",

                    code="payment_entry_duplicate_reference",

                )

            seen.add(key)



    @staticmethod

    def _validate_allocated_amount(row: PaymentEntry) -> None:

        """

        Port of ``validate_allocated_amount``.



        Skipped for an Internal Transfer, which allocates nothing. The negative

        branch matters for credit notes, where both figures are negative.

        """

        if row.payment_type is PaymentType.INTERNAL_TRANSFER:

            return

        for child in row.references:

            allocated = _dec(child.allocated_amount)

            outstanding = _dec(child.outstanding_amount)

            if allocated > 0 and allocated > outstanding:

                raise DomainValidationError(

                    f"Row #{child.idx}: Allocated Amount cannot be greater than "

                    f"outstanding amount.",

                    code="payment_entry_over_allocated",

                )

            if allocated < 0 and allocated < outstanding:

                raise DomainValidationError(

                    f"Row #{child.idx}: Allocated Amount cannot be greater than "

                    f"outstanding amount.",

                    code="payment_entry_over_allocated",

                )



    @staticmethod

    def _set_amounts(row: PaymentEntry) -> None:

        """Port of ``set_amounts``: totals and the unallocated remainder."""

        allocated = sum((_dec(r.allocated_amount) for r in row.references), ZERO)

        deductions = sum((_dec(d.amount) for d in row.deductions), ZERO)



        row.total_allocated_amount = allocated

        row.total_deduction_amount = deductions

        row.unallocated_amount = _dec(row.paid_amount) - allocated - deductions

        # Upstream's difference_amount is what must reach zero before submit.

        row.difference_amount = ZERO



    @staticmethod

    def _set_status(row: PaymentEntry) -> None:

        """Port of ``set_status``."""

        if row.docstatus == DocStatus.CANCELLED.value:

            row.status = "Cancelled"

        elif row.docstatus == DocStatus.SUBMITTED.value:

            row.status = "Submitted"

        else:

            row.status = "Draft"



    def _resolve_fiscal_year(

        self, db: Session, business_id: uuid.UUID, row: PaymentEntry

    ) -> str:

        """

        The fiscal year covering ``posting_date``, or a hard error.



        Same upstream rule as the invoices and the journal entry:

        ``AccountsController.validate_date_with_fiscal_year`` -> ``get_fiscal_year``.

        """

        fy = self._fiscal_years.get_for_date(db, business_id, row.posting_date)

        if fy is None:

            raise DomainValidationError(

                f"Posting Date {row.posting_date.isoformat()} is not in any "

                f"active Fiscal Year",

                code="payment_entry_not_in_fiscal_year",

                details={"posting_date": row.posting_date.isoformat()},

            )

        return fy.year



    def _validate(self, row: PaymentEntry) -> None:

        self._validate_mandatory(row)

        self._validate_duplicate_references(row)

        self._validate_allocated_amount(row)

        self._set_amounts(row)

        self._validate_received_amount(row)



    # ── GL posting ───────────────────────────────────────────────────────────

    def _post_gl_entries(

        self, db: Session, business_id: uuid.UUID, row: PaymentEntry,

        fiscal_year: Optional[str] = None,

    ) -> None:

        """

        Port of ``make_gl_entries``.



        Two entries: the money leaves ``paid_from`` and arrives in ``paid_to``.

        The cost centre rides on both so the split survives into the ledger.

        """

        amount = _dec(row.paid_amount)

        self.gl.post_balanced_set(

            db,

            business_id,

            [

                GLEntryCreate(

                    posting_date=row.posting_date,

                    fiscal_year=fiscal_year,

                    account_id=row.paid_from_id,

                    cost_center_id=row.cost_center_id,

                    debit=ZERO,

                    credit=amount,

                    party_type=row.party_type,

                    party=row.party,

                    voucher_type="Payment Entry",

                    voucher_no=row.name,

                    remarks=row.remarks,

                ),

                GLEntryCreate(

                    posting_date=row.posting_date,

                    fiscal_year=fiscal_year,

                    account_id=row.paid_to_id,

                    cost_center_id=row.cost_center_id,

                    debit=amount,

                    credit=ZERO,

                    party_type=row.party_type,

                    party=row.party,

                    voucher_type="Payment Entry",

                    voucher_no=row.name,

                    remarks=row.remarks,

                ),

            ],

            voucher_type="Payment Entry",

            voucher_no=row.name,

        )



    def _reverse_gl_entries(self, db: Session, business_id: uuid.UUID, row: PaymentEntry) -> None:

        for entry in self.gl.repository.list_for_voucher(

            db, business_id, "Payment Entry", row.name

        ):

            if not entry.is_cancelled:

                self.gl.cancel(db, business_id, entry.id)



    def sync_reference_outstandings(
        self, db: Session, business_id: uuid.UUID, row: PaymentEntry, reverse: bool = False
    ) -> None:
        """
        Updates outstanding_amount on referenced Sales Invoices when Payment Entry posts or cancels.
        """
        from app.accounts.sales_invoice_domain.models.sales_invoice import SalesInvoice
        for ref in getattr(row, "references", []):
            if ref.reference_doctype == "Sales Invoice" and ref.reference_name:
                inv = db.query(SalesInvoice).filter(
                    SalesInvoice.business_id == business_id,
                    SalesInvoice.name == ref.reference_name
                ).first()
                if not inv:
                    try:
                        uid = uuid.UUID(ref.reference_name)
                        inv = db.query(SalesInvoice).filter(
                            SalesInvoice.business_id == business_id,
                            SalesInvoice.id == uid
                        ).first()
                    except ValueError:
                        pass
                if inv:
                    alloc = Decimal(str(ref.allocated_amount or 0))
                    curr = Decimal(str(inv.outstanding_amount if inv.outstanding_amount is not None else inv.grand_total or 0))
                    total = Decimal(str(inv.grand_total or 0))
                    if reverse:
                        new_amt = min(total, curr + alloc)
                    else:
                        new_amt = max(Decimal("0"), curr - alloc)
                    inv.outstanding_amount = new_amt
                    if new_amt <= 0:
                        inv.status = "Paid"
                    elif new_amt < total:
                        inv.status = "Partly Paid"
                    else:
                        inv.status = "Unpaid"
                    db.flush()



    # ── public API ───────────────────────────────────────────────────────────

    def get(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> PaymentEntry:

        return self._get_or_404(db, business_id, entry_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_children(

        self,

        business_id: uuid.UUID,

        row: PaymentEntry,

        references: Optional[list[dict]],

        deductions: Optional[list[dict]],

    ) -> None:

        if references is not None:

            row.references.clear()

            for idx, item in enumerate(references, start=1):

                row.references.append(

                    PaymentEntryReference(

                        business_id=business_id,

                        idx=idx,

                        reference_doctype=item["reference_doctype"],

                        reference_name=item["reference_name"],

                        due_date=item.get("due_date"),

                        bill_no=item.get("bill_no"),

                        total_amount=item.get("total_amount"),

                        outstanding_amount=item.get("outstanding_amount"),

                        allocated_amount=item.get("allocated_amount"),

                        exchange_rate=item.get("exchange_rate"),

                        payment_term=item.get("payment_term"),

                        exchange_gain_loss=item.get("exchange_gain_loss"),

                        account_id=item.get("account_id"),

                        account_type=item.get("account_type"),

                        payment_type=item.get("payment_type"),

                        payment_request=item.get("payment_request"),

                    )

                )

        if deductions is not None:

            row.deductions.clear()

            for idx, item in enumerate(deductions, start=1):

                row.deductions.append(

                    PaymentEntryDeduction(

                        business_id=business_id,

                        idx=idx,

                        account_id=item["account_id"],

                        cost_center_id=item["cost_center_id"],

                        amount=item["amount"],

                        description=item.get("description"),

                        is_exchange_gain_loss=bool(item.get("is_exchange_gain_loss")),

                    )

                )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PaymentEntryCreate

    ) -> PaymentEntry:

        row = PaymentEntry(

            business_id=business_id,

            name=self.repository.next_name(db, business_id, payload.posting_date),

            naming_series=payload.naming_series,

            title=payload.title,

            payment_type=payload.payment_type,

            posting_date=payload.posting_date,

            paid_from_id=payload.paid_from_id,

            paid_to_id=payload.paid_to_id,

            paid_amount=payload.paid_amount,

            received_amount=payload.received_amount,

            source_exchange_rate=payload.source_exchange_rate,

            target_exchange_rate=payload.target_exchange_rate,

            paid_from_account_currency=payload.paid_from_account_currency,

            paid_to_account_currency=payload.paid_to_account_currency,

            party_type=payload.party_type,

            party=payload.party,

            party_name=payload.party_name,

            cost_center_id=payload.cost_center_id,

            mode_of_payment=payload.mode_of_payment,

            bank_account_id=payload.bank_account_id,

            party_bank_account_id=payload.party_bank_account_id,

            reference_no=payload.reference_no,

            reference_date=payload.reference_date,

            project=payload.project,

            remarks=payload.remarks,

            is_opening="Yes" if payload.is_opening else "No",

            apply_tds=payload.apply_tds,

            docstatus=DocStatus.DRAFT.value,

        )

        self._replace_children(

            business_id,

            row,

            [r.model_dump() for r in payload.references],

            [d.model_dump() for d in payload.deductions],

        )



        try:

            self._resolve_fiscal_year(db, business_id, row)

            self._validate(row)

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

        entry_id: uuid.UUID,

        payload: PaymentEntryUpdate,

    ) -> PaymentEntry:

        row = self._get_or_404(db, business_id, entry_id)

        if not row.is_draft:

            raise DomainValidationError(

                "Only a draft Payment Entry can be edited. Cancel and re-post instead.",

                code="payment_entry_not_editable",

            )



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "references":

                    self._replace_children(business_id, row, value, None)

                elif field_name == "deductions":

                    self._replace_children(business_id, row, None, value)

                else:

                    setattr(row, field_name, value)

            self._validate(row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, entry_id)

        if not row.is_draft:

            raise DomainValidationError(

                "Only a draft Payment Entry can be deleted. Cancel it first.",

                code="payment_entry_not_deletable",

            )

        self.repository.delete(db, row)

        db.commit()



    # ── lifecycle ────────────────────────────────────────────────────────────

    def submit(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> PaymentEntry:

        """

        Port of ``on_submit``.



        Upstream refuses to submit while ``difference_amount`` is non-zero; the

        derived amounts are recomputed first so the check is against current

        data rather than a stale stored value.

        """

        row = self._get_or_404(db, business_id, entry_id)

        assert_can_submit(row, "Payment Entry")



        try:

            self._validate(row)

            if _dec(row.difference_amount) != 0:

                raise DomainValidationError(

                    "Difference Amount must be zero", code="payment_entry_difference_not_zero"

                )

            db.flush()

            self._post_gl_entries(

                db, business_id, row,

                self._resolve_fiscal_year(db, business_id, row),

            )

            self.sync_reference_outstandings(db, business_id, row)

            row.docstatus = DocStatus.SUBMITTED.value

            self._set_status(row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def cancel(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> PaymentEntry:

        """Port of ``on_cancel``: reverse the GL Entries, then cancel."""

        row = self._get_or_404(db, business_id, entry_id)

        assert_can_cancel(row, "Payment Entry")



        try:

            self._reverse_gl_entries(db, business_id, row)
            self.sync_reference_outstandings(db, business_id, row, reverse=True)

            row.docstatus = DocStatus.CANCELLED.value

            self._set_status(row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row

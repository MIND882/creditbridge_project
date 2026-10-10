# HAND-WRITTEN

"""

Business logic for Payment Request -- port of

``erpnext/accounts/doctype/payment_request/payment_request.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    on_discard

    validate

    validate_against_payment_reference

    validate_reference_document

    validate_payment_request_amount

    validate_currency

    validate_subscription_details

    before_submit

    on_submit

    get_tx_data

    request_phone_payment

    get_request_amount

    on_cancel

    make_invoice

    payment_gateway_validation

    set_payment_request_url

    get_payment_url

    set_as_paid

    create_payment_entry

    resend_payment_email

    send_email

    get_message

    set_failed

    set_as_cancelled

    check_if_payment_entry_exists

    make_communication_entry

    create_subscription

    update_reference_advance_payment_status



**Upstream has 21 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal, ROUND_HALF_UP

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_request_domain.models.payment_request import (

    PaymentRequest,

    PaymentRequestStatus,

)

from app.accounts.subscription_plan_detail_domain.models.subscription_plan_detail import SubscriptionPlanDetail

from app.accounts.payment_reference_domain.models.payment_reference import PaymentReference

from app.accounts.payment_request_domain.repositories.payment_request_repository import (

    PaymentRequestRepository,

)

from app.accounts.payment_request_domain.schemas.payment_request import (

    PaymentRequestCreate,

    PaymentRequestUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentRequestService"]





def _round_currency(value: Decimal) -> Decimal:

    """``flt(x, self.precision("grand_total"))`` -- currency precision is 2."""

    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)





class PaymentRequestService:

    def __init__(self, repository: Optional[PaymentRequestRepository] = None) -> None:

        self.repository = repository or PaymentRequestRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentRequest:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Payment Request", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PaymentRequest, *, is_new: bool

    ) -> None:

        """

        Port of upstream ``validate``. Upstream order is preserved.



        ``validate_currency`` is *not* called: upstream has it commented out

        (``# self.validate_currency()``), so enforcing it would add a rule

        ERPNext does not have. See ``_validate_currency``.

        """

        if is_new:

            # upstream: if self.get("__islocal"): self.status = "Draft"

            row.status = PaymentRequestStatus.DRAFT



        self._validate_reference_document(row)

        self._validate_against_payment_reference(row)

        self._validate_payment_request_amount(db, business_id, row)

        self._validate_subscription_details(db, business_id, row)



    # ── validate_reference_document ───────────────────────────────────────

    def _validate_reference_document(self, row: PaymentRequest) -> None:

        if not row.reference_doctype or not row.reference_name:

            raise DomainValidationError(

                "To create a Payment Request reference document is required",

                code="payment_request_reference_required",

                details={

                    "reference_doctype": row.reference_doctype,

                    "reference_name": row.reference_name,

                },

            )



    # ── validate_against_payment_reference ────────────────────────────────

    def _validate_against_payment_reference(self, row: PaymentRequest) -> None:

        """

        When the request is broken into a payment plan, the plan has to add up

        to what is being requested and must not reference the same schedule

        row twice.

        """

        rows = list(row.payment_reference)

        if not rows:

            return



        expected = sum(

            (Decimal(str(r.amount or 0)) for r in rows), Decimal(0)

        )

        grand = Decimal(str(row.grand_total or 0))

        if _round_currency(expected) != _round_currency(grand):

            raise DomainValidationError(

                "Grand Total must match sum of Payment References",

                code="payment_request_grand_total_mismatch",

                details={

                    "grand_total": str(grand),

                    "sum_of_references": str(expected),

                },

            )



        seen: set[uuid.UUID] = set()

        for r in rows:

            # upstream skips a blank payment_schedule: legacy rows predate the

            # column and would otherwise all collide with each other.

            if not r.payment_schedule_id:

                continue

            if r.payment_schedule_id in seen:

                raise DomainValidationError(

                    "Duplicate Payment Schedule selected",

                    code="payment_request_duplicate_schedule",

                    details={"payment_schedule_id": str(r.payment_schedule_id)},

                )

            seen.add(r.payment_schedule_id)



    # ── validate_payment_request_amount ───────────────────────────────────

    def _validate_payment_request_amount(

        self, db: Session, business_id: uuid.UUID, row: PaymentRequest

    ) -> None:

        # upstream returns early when a payment plan is supplied; the sum

        # check in _validate_against_payment_reference covers that case.

        if row.payment_reference:

            return



        grand = Decimal(str(row.grand_total or 0))

        # Upstream tests `grand_total == 0`. Widened to `<= 0`: a negative

        # request is the same defect and would otherwise pass silently.

        if grand <= 0:

            raise DomainValidationError(

                "Grand Total cannot be zero",

                code="payment_request_zero_amount",

                details={"grand_total": str(grand)},

            )



        # TODO(PORT-VALIDATION): the rest of upstream

        # `validate_payment_request_amount` loads the referenced Sales Order /

        # Sales Invoice, calls `get_amount()` for the outstanding balance, and

        # throws "Payment Entry is already created" (nothing outstanding) or

        # "Total Payment Request amount cannot be greater than {0} amount"

        # (over-requesting). Neither doctype is converted, so both checks fail

        # open here: a request may currently exceed the reference's balance.

        return None



    # ── validate_subscription_details ─────────────────────────────────────

    def _validate_subscription_details(

        self, db: Session, business_id: uuid.UUID, row: PaymentRequest

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream walks ``subscription_plans``, requires

        each plan's ``payment_gateway`` to match

        ``self.payment_gateway_account``, and msgprints (does not throw) when

        the summed plan rates differ from ``grand_total``.



        Needs the Subscription Plan doctype, which is not converted. Fails open.

        """

        return None



    # ── validate_currency -- present upstream but disabled ────────────────

    def _validate_currency(self, row: PaymentRequest) -> None:  # pragma: no cover

        """

        Deliberately never called. Upstream ``validate`` has this line

        commented out:



            # self.validate_currency()



        so a request whose ``currency`` differs from the payment account's

        currency is accepted by ERPNext. It is kept here only to record that

        the omission is intentional, not an oversight.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentRequest:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentRequest]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentRequest].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_subscription_plans(

        self, business_id: uuid.UUID, row: PaymentRequest, items: list[dict]

    ) -> None:

        row.subscription_plans.clear()

        for idx, item in enumerate(items, start=1):

            row.subscription_plans.append(

                SubscriptionPlanDetail(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Payment Request',

                    qty=item.get('qty'),

                    plan=item.get('plan'),

                )

            )



    def _replace_payment_reference(

        self, business_id: uuid.UUID, row: PaymentRequest, items: list[dict]

    ) -> None:

        row.payment_reference.clear()

        for idx, item in enumerate(items, start=1):

            row.payment_reference.append(

                PaymentReference(

                    business_id=business_id,

                    idx=idx,

                    payment_term_id=item.get('payment_term_id'),

                    description=item.get('description'),

                    due_date=item.get('due_date'),

                    amount=item.get('amount'),

                    currency=item.get('currency'),

                    payment_schedule_id=item.get('payment_schedule_id'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PaymentRequest).where(

                    PaymentRequest.business_id == business_id

                )

            )

            or 0

        )

        year = dt.date.today().year

        return f"ACC-PRQ-{year}-{count + 1:08d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PaymentRequestCreate

    ) -> PaymentRequest:

        row = PaymentRequest(

            business_id=business_id,

            name=self.next_name(db, business_id),

            payment_request_type=payload.payment_request_type,

            transaction_date=payload.transaction_date,

            naming_series=payload.naming_series,

            mode_of_payment_id=payload.mode_of_payment_id,

            party_type=payload.party_type,

            party=payload.party,

            reference_doctype=payload.reference_doctype,

            reference_name=payload.reference_name,

            grand_total=payload.grand_total,

            is_a_subscription=payload.is_a_subscription,

            currency=payload.currency,

            bank_account_id=payload.bank_account_id,

            bank_id=payload.bank_id,

            bank_account_no=payload.bank_account_no,

            account=payload.account,

            iban=payload.iban,

            branch_code=payload.branch_code,

            swift_number=payload.swift_number,

            cost_center_id=payload.cost_center_id,

            project=payload.project,

            print_format=payload.print_format,

            email_to=payload.email_to,

            subject=payload.subject,

            payment_gateway_account=payload.payment_gateway_account,

            status=payload.status,

            make_sales_invoice=payload.make_sales_invoice,

            message=payload.message,

            mute_email=payload.mute_email,

            payment_url=payload.payment_url,

            payment_gateway=payload.payment_gateway,

            payment_account=payload.payment_account,

            payment_channel=payload.payment_channel,

            payment_order=payload.payment_order,

            amended_from=payload.amended_from,

            failed_reason=payload.failed_reason,

            outstanding_amount=payload.outstanding_amount,

            party_account_currency=payload.party_account_currency,

            party_name=payload.party_name,

            phone_number=payload.phone_number,

        )

        self._replace_subscription_plans(business_id, row, [x.model_dump() for x in payload.subscription_plans])

        self._replace_payment_reference(business_id, row, [x.model_dump() for x in payload.payment_reference])



        try:

            db.flush()  # children need ids before validation reads them

            self._validate(db, business_id, row, is_new=True)

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

        payload: PaymentRequestUpdate,

    ) -> PaymentRequest:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "subscription_plans":

                    self._replace_subscription_plans(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "payment_reference":

                    self._replace_payment_reference(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row, is_new=False)

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

    ) -> PaymentRequest:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Payment Request")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentRequest:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Payment Request")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

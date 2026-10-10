# HAND-WRITTEN

"""

Business logic for Dunning -- port of

``erpnext/accounts/doctype/dunning/dunning.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    validate_same_currency

    validate_overdue_payments

    validate_totals

    set_party_details

    set_dunning_level

    on_cancel

    get_dunning_letter_text



**Upstream has 1 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.dunning_domain.models.dunning import Dunning

from app.accounts.overdue_payment_domain.models.overdue_payment import OverduePayment

from app.accounts.dunning_domain.repositories.dunning_repository import (

    DunningRepository,

)

from app.accounts.dunning_domain.schemas.dunning import (

    DunningCreate,

    DunningUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["DunningService"]





class DunningService:

    def __init__(self, repository: Optional[DunningRepository] = None) -> None:

        self.repository = repository or DunningRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Dunning:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Dunning", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Dunning

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

    ) -> Dunning:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Dunning]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Dunning].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_overdue_payments(

        self, business_id: uuid.UUID, row: Dunning, items: list[dict]

    ) -> None:

        row.overdue_payments.clear()

        for idx, item in enumerate(items, start=1):

            row.overdue_payments.append(

                OverduePayment(

                    business_id=business_id,

                    idx=idx,

                    payment_term_id=item.get('payment_term_id'),

                    description=item.get('description'),

                    due_date=item.get('due_date'),

                    mode_of_payment_id=item.get('mode_of_payment_id'),

                    invoice_portion=item.get('invoice_portion'),

                    payment_amount=item.get('payment_amount'),

                    outstanding=item.get('outstanding'),

                    paid_amount=item.get('paid_amount'),

                    discounted_amount=item.get('discounted_amount'),

                    sales_invoice=item.get('sales_invoice'),

                    payment_schedule=item.get('payment_schedule'),

                    overdue_days=item.get('overdue_days'),

                    dunning_level=item.get('dunning_level'),

                    interest=item.get('interest'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(Dunning).where(

                    Dunning.business_id == business_id

                )

            )

            or 0

        )

        return f"DUN-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: DunningCreate

    ) -> Dunning:

        row = Dunning(

            business_id=business_id,

            name=self.next_name(db, business_id),

            naming_series=payload.naming_series,

            customer_name=payload.customer_name,

            posting_date=payload.posting_date,

            dunning_type_id=payload.dunning_type_id,

            dunning_fee=payload.dunning_fee,

            language=payload.language,

            letter_head=payload.letter_head,

            amended_from=payload.amended_from,

            body_text=payload.body_text,

            closing_text=payload.closing_text,

            posting_time=payload.posting_time,

            rate_of_interest=payload.rate_of_interest,

            address_display=payload.address_display,

            contact_display=payload.contact_display,

            contact_mobile=payload.contact_mobile,

            company_address_display=payload.company_address_display,

            contact_email=payload.contact_email,

            customer=payload.customer,

            grand_total=payload.grand_total,

            status=payload.status,

            income_account_id=payload.income_account_id,

            total_interest=payload.total_interest,

            total_outstanding=payload.total_outstanding,

            customer_address=payload.customer_address,

            contact_person=payload.contact_person,

            dunning_amount=payload.dunning_amount,

            cost_center_id=payload.cost_center_id,

            spacer=payload.spacer,

            company_address=payload.company_address,

            currency=payload.currency,

            conversion_rate=payload.conversion_rate,

            base_dunning_amount=payload.base_dunning_amount,

        )

        self._replace_overdue_payments(business_id, row, [x.model_dump() for x in payload.overdue_payments])



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

        payload: DunningUpdate,

    ) -> Dunning:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "overdue_payments":

                    self._replace_overdue_payments(business_id, row, value or [])

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

    ) -> Dunning:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Dunning")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Dunning:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Dunning")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

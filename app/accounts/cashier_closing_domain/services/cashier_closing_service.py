# HAND-WRITTEN

"""

Business logic for Cashier Closing -- port of

``erpnext/accounts/doctype/cashier_closing/cashier_closing.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    before_save

    get_outstanding

    make_calculations

    validate_time



**Upstream has 1 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.cashier_closing_domain.models.cashier_closing import CashierClosing

from app.accounts.cashier_closing_payments_domain.models.cashier_closing_payments import CashierClosingPayments

from app.accounts.cashier_closing_domain.repositories.cashier_closing_repository import (

    CashierClosingRepository,

)

from app.accounts.cashier_closing_domain.schemas.cashier_closing import (

    CashierClosingCreate,

    CashierClosingUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["CashierClosingService"]





class CashierClosingService:

    def __init__(self, repository: Optional[CashierClosingRepository] = None) -> None:

        self.repository = repository or CashierClosingRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> CashierClosing:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Cashier Closing", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: CashierClosing

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

    ) -> CashierClosing:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[CashierClosing]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[CashierClosing].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_payments(

        self, business_id: uuid.UUID, row: CashierClosing, items: list[dict]

    ) -> None:

        row.payments.clear()

        for idx, item in enumerate(items, start=1):

            row.payments.append(

                CashierClosingPayments(

                    business_id=business_id,

                    idx=idx,

                    mode_of_payment_id=item.get('mode_of_payment_id'),

                    amount=item.get('amount'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(CashierClosing).where(

                    CashierClosing.business_id == business_id

                )

            )

            or 0

        )

        return f"CAS-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: CashierClosingCreate

    ) -> CashierClosing:

        row = CashierClosing(

            business_id=business_id,

            name=self.next_name(db, business_id),

            naming_series=payload.naming_series,

            user=payload.user,

            date=payload.date,

            from_time=payload.from_time,

            time=payload.time,

            expense=payload.expense,

            custody=payload.custody,

            returns=payload.returns,

            outstanding_amount=payload.outstanding_amount,

            net_amount=payload.net_amount,

            amended_from=payload.amended_from,

        )

        self._replace_payments(business_id, row, [x.model_dump() for x in payload.payments])



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

        payload: CashierClosingUpdate,

    ) -> CashierClosing:

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

    ) -> CashierClosing:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Cashier Closing")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> CashierClosing:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Cashier Closing")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

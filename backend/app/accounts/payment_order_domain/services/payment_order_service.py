# HAND-WRITTEN

"""

Business logic for Payment Order -- port of

``erpnext/accounts/doctype/payment_order/payment_order.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    on_submit

    on_cancel

    update_payment_status



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_order_domain.models.payment_order import PaymentOrder

from app.accounts.payment_order_reference_domain.models.payment_order_reference import PaymentOrderReference

from app.accounts.payment_order_domain.repositories.payment_order_repository import (

    PaymentOrderRepository,

)

from app.accounts.payment_order_domain.schemas.payment_order import (

    PaymentOrderCreate,

    PaymentOrderUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentOrderService"]





class PaymentOrderService:

    def __init__(self, repository: Optional[PaymentOrderRepository] = None) -> None:

        self.repository = repository or PaymentOrderRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentOrder:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Payment Order", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PaymentOrder

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentOrder:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentOrder]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentOrder].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_references(

        self, business_id: uuid.UUID, row: PaymentOrder, items: list[dict]

    ) -> None:

        row.references.clear()

        for idx, item in enumerate(items, start=1):

            row.references.append(

                PaymentOrderReference(

                    business_id=business_id,

                    idx=idx,

                    reference_doctype=item.get('reference_doctype'),

                    reference_name=item.get('reference_name'),

                    amount=item.get('amount'),

                    supplier=item.get('supplier'),

                    payment_request=item.get('payment_request'),

                    mode_of_payment_id=item.get('mode_of_payment_id'),

                    bank_account_id=item.get('bank_account_id'),

                    account_id=item.get('account_id'),

                    payment_reference=item.get('payment_reference'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PaymentOrder).where(

                    PaymentOrder.business_id == business_id

                )

            )

            or 0

        )

        return f"PAY-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PaymentOrderCreate

    ) -> PaymentOrder:

        row = PaymentOrder(

            business_id=business_id,

            name=self.next_name(db, business_id),

            naming_series=payload.naming_series,

            party=payload.party,

            posting_date=payload.posting_date,

            amended_from=payload.amended_from,

            payment_order_type=payload.payment_order_type,

            company_bank_account_id=payload.company_bank_account_id,

            company_bank_id=payload.company_bank_id,

            account=payload.account,

        )

        self._replace_references(business_id, row, [x.model_dump() for x in payload.references])



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

        payload: PaymentOrderUpdate,

    ) -> PaymentOrder:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "references":

                    self._replace_references(business_id, row, value or [])

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

    ) -> PaymentOrder:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Payment Order")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentOrder:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Payment Order")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

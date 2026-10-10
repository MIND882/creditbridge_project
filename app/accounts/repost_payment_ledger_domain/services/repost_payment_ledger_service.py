# HAND-WRITTEN

"""

Business logic for Repost Payment Ledger -- port of

``erpnext/accounts/doctype/repost_payment_ledger/repost_payment_ledger.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    before_validate

    load_vouchers_based_on_filters

    get_vouchers

    set_status

    on_submit



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.repost_payment_ledger_domain.models.repost_payment_ledger import RepostPaymentLedger

from app.accounts.repost_payment_ledger_items_domain.models.repost_payment_ledger_items import RepostPaymentLedgerItems

from app.accounts.repost_payment_ledger_domain.repositories.repost_payment_ledger_repository import (

    RepostPaymentLedgerRepository,

)

from app.accounts.repost_payment_ledger_domain.schemas.repost_payment_ledger import (

    RepostPaymentLedgerCreate,

    RepostPaymentLedgerUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["RepostPaymentLedgerService"]





class RepostPaymentLedgerService:

    def __init__(self, repository: Optional[RepostPaymentLedgerRepository] = None) -> None:

        self.repository = repository or RepostPaymentLedgerRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostPaymentLedger:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Repost Payment Ledger", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: RepostPaymentLedger

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostPaymentLedger:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[RepostPaymentLedger]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[RepostPaymentLedger].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_repost_vouchers(

        self, business_id: uuid.UUID, row: RepostPaymentLedger, items: list[dict]

    ) -> None:

        row.repost_vouchers.clear()

        for idx, item in enumerate(items, start=1):

            row.repost_vouchers.append(

                RepostPaymentLedgerItems(

                    business_id=business_id,

                    idx=idx,

                    voucher_type=item.get('voucher_type'),

                    voucher_no=item.get('voucher_no'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(RepostPaymentLedger).where(

                    RepostPaymentLedger.business_id == business_id

                )

            )

            or 0

        )

        return f"REP-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: RepostPaymentLedgerCreate

    ) -> RepostPaymentLedger:

        row = RepostPaymentLedger(

            business_id=business_id,

            name=self.next_name(db, business_id),

            posting_date=payload.posting_date,

            voucher_type=payload.voucher_type,

            amended_from=payload.amended_from,

            repost_status=payload.repost_status,

            add_manually=payload.add_manually,

            repost_error_log=payload.repost_error_log,

        )

        self._replace_repost_vouchers(business_id, row, [x.model_dump() for x in payload.repost_vouchers])



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

        payload: RepostPaymentLedgerUpdate,

    ) -> RepostPaymentLedger:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "repost_vouchers":

                    self._replace_repost_vouchers(business_id, row, value or [])

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

    ) -> RepostPaymentLedger:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Repost Payment Ledger")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostPaymentLedger:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Repost Payment Ledger")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

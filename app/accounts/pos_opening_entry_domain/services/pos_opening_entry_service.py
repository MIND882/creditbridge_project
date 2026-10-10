# HAND-WRITTEN

"""

Business logic for POS Opening Entry -- port of

``erpnext/accounts/doctype/pos_opening_entry/pos_opening_entry.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    validate_pos_profile_and_cashier

    check_open_pos_exists

    check_user_already_assigned

    validate_payment_method_account

    on_submit

    before_cancel

    on_cancel

    check_poe_is_cancellable



**Upstream has 8 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_opening_entry_domain.models.pos_opening_entry import POSOpeningEntry

from app.accounts.pos_opening_entry_detail_domain.models.pos_opening_entry_detail import POSOpeningEntryDetail

from app.accounts.pos_opening_entry_domain.repositories.pos_opening_entry_repository import (

    POSOpeningEntryRepository,

)

from app.accounts.pos_opening_entry_domain.schemas.pos_opening_entry import (

    POSOpeningEntryCreate,

    POSOpeningEntryUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSOpeningEntryService"]





class POSOpeningEntryService:

    def __init__(self, repository: Optional[POSOpeningEntryRepository] = None) -> None:

        self.repository = repository or POSOpeningEntryRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSOpeningEntry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Opening Entry", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: POSOpeningEntry

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **8 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSOpeningEntry:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSOpeningEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSOpeningEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_balance_details(

        self, business_id: uuid.UUID, row: POSOpeningEntry, items: list[dict]

    ) -> None:

        row.balance_details.clear()

        for idx, item in enumerate(items, start=1):

            row.balance_details.append(

                POSOpeningEntryDetail(

                    business_id=business_id,

                    idx=idx,

                    mode_of_payment_id=item.get('mode_of_payment_id'),

                    opening_amount=item.get('opening_amount'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(POSOpeningEntry).where(

                    POSOpeningEntry.business_id == business_id

                )

            )

            or 0

        )

        return f"POS-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: POSOpeningEntryCreate

    ) -> POSOpeningEntry:

        row = POSOpeningEntry(

            business_id=business_id,

            name=self.next_name(db, business_id),

            period_start_date=payload.period_start_date,

            period_end_date=payload.period_end_date,

            posting_date=payload.posting_date,

            pos_profile=payload.pos_profile,

            user=payload.user,

            amended_from=payload.amended_from,

            set_posting_date=payload.set_posting_date,

            status=payload.status,

            pos_closing_entry=payload.pos_closing_entry,

        )

        self._replace_balance_details(business_id, row, [x.model_dump() for x in payload.balance_details])



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

        payload: POSOpeningEntryUpdate,

    ) -> POSOpeningEntry:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "balance_details":

                    self._replace_balance_details(business_id, row, value or [])

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

    ) -> POSOpeningEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "POS Opening Entry")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSOpeningEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "POS Opening Entry")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

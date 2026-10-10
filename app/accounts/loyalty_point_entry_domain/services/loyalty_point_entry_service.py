# HAND-WRITTEN

"""

Business logic for Loyalty Point Entry -- port of

``erpnext/accounts/doctype/loyalty_point_entry/loyalty_point_entry.py``.







Upstream hooks:

    (none -- upstream's controller defines no hooks)



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.loyalty_point_entry_domain.models.loyalty_point_entry import LoyaltyPointEntry

from app.accounts.loyalty_point_entry_domain.repositories.loyalty_point_entry_repository import (

    LoyaltyPointEntryRepository,

)

from app.accounts.loyalty_point_entry_domain.schemas.loyalty_point_entry import (

    LoyaltyPointEntryCreate,

    LoyaltyPointEntryUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["LoyaltyPointEntryService"]





class LoyaltyPointEntryService:

    def __init__(self, repository: Optional[LoyaltyPointEntryRepository] = None) -> None:

        self.repository = repository or LoyaltyPointEntryRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LoyaltyPointEntry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Loyalty Point Entry", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: LoyaltyPointEntry

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LoyaltyPointEntry:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LoyaltyPointEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LoyaltyPointEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(LoyaltyPointEntry).where(

                    LoyaltyPointEntry.business_id == business_id

                )

            )

            or 0

        )

        return f"LOY-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: LoyaltyPointEntryCreate

    ) -> LoyaltyPointEntry:

        row = LoyaltyPointEntry(

            business_id=business_id,

            name=self.next_name(db, business_id),

            loyalty_program=payload.loyalty_program,

            loyalty_program_tier=payload.loyalty_program_tier,

            customer=payload.customer,

            redeem_against=payload.redeem_against,

            loyalty_points=payload.loyalty_points,

            purchase_amount=payload.purchase_amount,

            expiry_date=payload.expiry_date,

            posting_date=payload.posting_date,

            invoice_type=payload.invoice_type,

            invoice=payload.invoice,

            discretionary_reason=payload.discretionary_reason,

        )



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

        payload: LoyaltyPointEntryUpdate,

    ) -> LoyaltyPointEntry:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

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

# HAND-WRITTEN

"""

Business logic for Ledger Health -- port of

``erpnext/accounts/doctype/ledger_health/ledger_health.py``.







Upstream hooks:

    (none -- upstream's controller defines no hooks)



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.ledger_health_domain.models.ledger_health import LedgerHealth

from app.accounts.ledger_health_domain.repositories.ledger_health_repository import (

    LedgerHealthRepository,

)

from app.accounts.ledger_health_domain.schemas.ledger_health import (

    LedgerHealthCreate,

    LedgerHealthUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["LedgerHealthService"]





class LedgerHealthService:

    def __init__(self, repository: Optional[LedgerHealthRepository] = None) -> None:

        self.repository = repository or LedgerHealthRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LedgerHealth:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Ledger Health", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: LedgerHealth

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LedgerHealth:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LedgerHealth]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LedgerHealth].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(LedgerHealth).where(

                    LedgerHealth.business_id == business_id

                )

            )

            or 0

        )

        return f"LED-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: LedgerHealthCreate

    ) -> LedgerHealth:

        row = LedgerHealth(

            business_id=business_id,

            name=self.next_name(db, business_id),

            voucher_type=payload.voucher_type,

            voucher_no=payload.voucher_no,

            debit_credit_mismatch=payload.debit_credit_mismatch,

            checked_on=payload.checked_on,

            general_and_payment_ledger_mismatch=payload.general_and_payment_ledger_mismatch,

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

        payload: LedgerHealthUpdate,

    ) -> LedgerHealth:

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

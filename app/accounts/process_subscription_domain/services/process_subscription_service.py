# HAND-WRITTEN

"""

Business logic for Process Subscription -- port of

``erpnext/accounts/doctype/process_subscription/process_subscription.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    on_submit

    process_all_subscription



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_subscription_domain.models.process_subscription import ProcessSubscription

from app.accounts.process_subscription_domain.repositories.process_subscription_repository import (

    ProcessSubscriptionRepository,

)

from app.accounts.process_subscription_domain.schemas.process_subscription import (

    ProcessSubscriptionCreate,

    ProcessSubscriptionUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProcessSubscriptionService"]





class ProcessSubscriptionService:

    def __init__(self, repository: Optional[ProcessSubscriptionRepository] = None) -> None:

        self.repository = repository or ProcessSubscriptionRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessSubscription:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Process Subscription", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ProcessSubscription

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessSubscription:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProcessSubscription]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProcessSubscription].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ProcessSubscription).where(

                    ProcessSubscription.business_id == business_id

                )

            )

            or 0

        )

        return f"PRO-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ProcessSubscriptionCreate

    ) -> ProcessSubscription:

        row = ProcessSubscription(

            business_id=business_id,

            name=self.next_name(db, business_id),

            amended_from=payload.amended_from,

            posting_date=payload.posting_date,

            subscription=payload.subscription,

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

        payload: ProcessSubscriptionUpdate,

    ) -> ProcessSubscription:

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessSubscription:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Process Subscription")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessSubscription:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Process Subscription")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row

# HAND-WRITTEN

"""

Business logic for Subscription Settings -- port of

``erpnext/accounts/doctype/subscription_settings/subscription_settings.py``.







Upstream hooks:

    (none -- upstream's controller defines no hooks)



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.subscription_settings_domain.models.subscription_settings import SubscriptionSettings

from app.accounts.subscription_settings_domain.repositories.subscription_settings_repository import (

    SubscriptionSettingsRepository,

)

from app.accounts.subscription_settings_domain.schemas.subscription_settings import (

    SubscriptionSettingsCreate,

    SubscriptionSettingsUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SubscriptionSettingsService"]





class SubscriptionSettingsService:

    def __init__(self, repository: Optional[SubscriptionSettingsRepository] = None) -> None:

        self.repository = repository or SubscriptionSettingsRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SubscriptionSettings:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Subscription Settings", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SubscriptionSettings

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SubscriptionSettings:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SubscriptionSettings]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SubscriptionSettings].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(SubscriptionSettings).where(

                    SubscriptionSettings.business_id == business_id

                )

            )

            or 0

        )

        return f"SUB-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SubscriptionSettingsCreate

    ) -> SubscriptionSettings:

        row = SubscriptionSettings(

            business_id=business_id,

            name=self.next_name(db, business_id),

            grace_period=payload.grace_period,

            cancel_after_grace=payload.cancel_after_grace,

            prorate=payload.prorate,

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

        payload: SubscriptionSettingsUpdate,

    ) -> SubscriptionSettings:

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

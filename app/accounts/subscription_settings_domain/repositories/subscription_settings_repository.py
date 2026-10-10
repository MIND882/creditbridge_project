"""Data access for SubscriptionSettings. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.subscription_settings_domain.models.subscription_settings import SubscriptionSettings

from app.core.pagination import normalise_paging



__all__ = ["SubscriptionSettingsRepository"]





class SubscriptionSettingsRepository:

    model = SubscriptionSettings





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SubscriptionSettings]:

        return db.scalar(

            select(SubscriptionSettings).where(

                SubscriptionSettings.business_id == business_id, SubscriptionSettings.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SubscriptionSettings]:

        return db.scalar(

            select(SubscriptionSettings).where(

                SubscriptionSettings.business_id == business_id, SubscriptionSettings.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[SubscriptionSettings], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SubscriptionSettings.business_id == business_id]

        if search:

            conditions.append(SubscriptionSettings.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SubscriptionSettings).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SubscriptionSettings)

            .where(*conditions)

            .order_by(SubscriptionSettings.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SubscriptionSettings) -> SubscriptionSettings:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SubscriptionSettings) -> None:

        db.delete(row)

        db.flush()

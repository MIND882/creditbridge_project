"""Data access for POSProfile. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.pos_profile_domain.models.pos_profile import POSProfile

from app.core.pagination import normalise_paging



__all__ = ["POSProfileRepository"]





class POSProfileRepository:

    model = POSProfile



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(POSProfile.applicable_for_users), selectinload(POSProfile.payments), selectinload(POSProfile.item_groups), selectinload(POSProfile.customer_groups)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSProfile]:

        return db.scalar(

            select(POSProfile).where(

                POSProfile.business_id == business_id, POSProfile.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[POSProfile]:

        return db.scalar(

            select(POSProfile).where(

                POSProfile.business_id == business_id, POSProfile.name == name

            ).options(*self._options())

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[POSProfile], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSProfile.business_id == business_id]

        if search:

            conditions.append(POSProfile.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(POSProfile).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSProfile)

            .where(*conditions)

            .order_by(POSProfile.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: POSProfile) -> POSProfile:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: POSProfile) -> None:

        db.delete(row)

        db.flush()

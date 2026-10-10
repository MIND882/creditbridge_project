"""Data access for POSSettings. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.pos_settings_domain.models.pos_settings import POSSettings

from app.core.pagination import normalise_paging



__all__ = ["POSSettingsRepository"]





class POSSettingsRepository:

    model = POSSettings



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(POSSettings.invoice_fields), selectinload(POSSettings.pos_search_fields)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSSettings]:

        return db.scalar(

            select(POSSettings).where(

                POSSettings.business_id == business_id, POSSettings.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[POSSettings]:

        return db.scalar(

            select(POSSettings).where(

                POSSettings.business_id == business_id, POSSettings.name == name

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

    ) -> tuple[Sequence[POSSettings], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSSettings.business_id == business_id]

        if search:

            conditions.append(POSSettings.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(POSSettings).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSSettings)

            .where(*conditions)

            .order_by(POSSettings.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: POSSettings) -> POSSettings:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: POSSettings) -> None:

        db.delete(row)

        db.flush()

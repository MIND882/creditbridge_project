"""Data access for POSOpeningEntry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.pos_opening_entry_domain.models.pos_opening_entry import POSOpeningEntry

from app.core.pagination import normalise_paging



__all__ = ["POSOpeningEntryRepository"]





class POSOpeningEntryRepository:

    model = POSOpeningEntry



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(POSOpeningEntry.balance_details)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSOpeningEntry]:

        return db.scalar(

            select(POSOpeningEntry).where(

                POSOpeningEntry.business_id == business_id, POSOpeningEntry.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[POSOpeningEntry]:

        return db.scalar(

            select(POSOpeningEntry).where(

                POSOpeningEntry.business_id == business_id, POSOpeningEntry.name == name

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

        include_cancelled: bool = False,

    ) -> tuple[Sequence[POSOpeningEntry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSOpeningEntry.business_id == business_id]

        if not include_cancelled:

            conditions.append(POSOpeningEntry.docstatus != 2)

        if search:

            conditions.append(POSOpeningEntry.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(POSOpeningEntry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSOpeningEntry)

            .where(*conditions)

            .order_by(POSOpeningEntry.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: POSOpeningEntry) -> POSOpeningEntry:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: POSOpeningEntry) -> None:

        db.delete(row)

        db.flush()

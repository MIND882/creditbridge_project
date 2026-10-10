"""Data access for Dunning. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.dunning_domain.models.dunning import Dunning

from app.core.pagination import normalise_paging



__all__ = ["DunningRepository"]





class DunningRepository:

    model = Dunning



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(Dunning.overdue_payments)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Dunning]:

        return db.scalar(

            select(Dunning).where(

                Dunning.business_id == business_id, Dunning.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Dunning]:

        return db.scalar(

            select(Dunning).where(

                Dunning.business_id == business_id, Dunning.name == name

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

    ) -> tuple[Sequence[Dunning], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Dunning.business_id == business_id]

        if not include_cancelled:

            conditions.append(Dunning.docstatus != 2)

        if search:

            conditions.append(Dunning.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Dunning).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Dunning)

            .where(*conditions)

            .order_by(Dunning.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: Dunning) -> Dunning:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Dunning) -> None:

        db.delete(row)

        db.flush()

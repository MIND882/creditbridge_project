"""Data access for LedgerMerge. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.ledger_merge_domain.models.ledger_merge import LedgerMerge

from app.core.pagination import normalise_paging



__all__ = ["LedgerMergeRepository"]





class LedgerMergeRepository:

    model = LedgerMerge



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(LedgerMerge.merge_accounts)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LedgerMerge]:

        return db.scalar(

            select(LedgerMerge).where(

                LedgerMerge.business_id == business_id, LedgerMerge.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[LedgerMerge]:

        return db.scalar(

            select(LedgerMerge).where(

                LedgerMerge.business_id == business_id, LedgerMerge.name == name

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

    ) -> tuple[Sequence[LedgerMerge], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LedgerMerge.business_id == business_id]

        if search:

            conditions.append(LedgerMerge.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(LedgerMerge).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LedgerMerge)

            .where(*conditions)

            .order_by(LedgerMerge.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: LedgerMerge) -> LedgerMerge:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: LedgerMerge) -> None:

        db.delete(row)

        db.flush()

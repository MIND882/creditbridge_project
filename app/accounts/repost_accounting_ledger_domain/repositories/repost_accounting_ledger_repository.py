"""Data access for RepostAccountingLedger. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.repost_accounting_ledger_domain.models.repost_accounting_ledger import RepostAccountingLedger

from app.core.pagination import normalise_paging



__all__ = ["RepostAccountingLedgerRepository"]





class RepostAccountingLedgerRepository:

    model = RepostAccountingLedger



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(RepostAccountingLedger.vouchers)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[RepostAccountingLedger]:

        return db.scalar(

            select(RepostAccountingLedger).where(

                RepostAccountingLedger.business_id == business_id, RepostAccountingLedger.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[RepostAccountingLedger]:

        return db.scalar(

            select(RepostAccountingLedger).where(

                RepostAccountingLedger.business_id == business_id, RepostAccountingLedger.name == name

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

    ) -> tuple[Sequence[RepostAccountingLedger], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [RepostAccountingLedger.business_id == business_id]

        if not include_cancelled:

            conditions.append(RepostAccountingLedger.docstatus != 2)

        if search:

            conditions.append(RepostAccountingLedger.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(RepostAccountingLedger).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(RepostAccountingLedger)

            .where(*conditions)

            .order_by(RepostAccountingLedger.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: RepostAccountingLedger) -> RepostAccountingLedger:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: RepostAccountingLedger) -> None:

        db.delete(row)

        db.flush()

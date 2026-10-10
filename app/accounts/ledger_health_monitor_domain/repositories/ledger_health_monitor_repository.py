"""Data access for LedgerHealthMonitor. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.ledger_health_monitor_domain.models.ledger_health_monitor import LedgerHealthMonitor

from app.core.pagination import normalise_paging



__all__ = ["LedgerHealthMonitorRepository"]





class LedgerHealthMonitorRepository:

    model = LedgerHealthMonitor



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(LedgerHealthMonitor.companies)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LedgerHealthMonitor]:

        return db.scalar(

            select(LedgerHealthMonitor).where(

                LedgerHealthMonitor.business_id == business_id, LedgerHealthMonitor.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[LedgerHealthMonitor]:

        return db.scalar(

            select(LedgerHealthMonitor).where(

                LedgerHealthMonitor.business_id == business_id, LedgerHealthMonitor.name == name

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

    ) -> tuple[Sequence[LedgerHealthMonitor], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LedgerHealthMonitor.business_id == business_id]

        if search:

            conditions.append(LedgerHealthMonitor.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(LedgerHealthMonitor).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LedgerHealthMonitor)

            .where(*conditions)

            .order_by(LedgerHealthMonitor.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: LedgerHealthMonitor) -> LedgerHealthMonitor:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: LedgerHealthMonitor) -> None:

        db.delete(row)

        db.flush()

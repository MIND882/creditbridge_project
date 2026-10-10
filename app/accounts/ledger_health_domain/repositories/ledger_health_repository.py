"""Data access for LedgerHealth. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.ledger_health_domain.models.ledger_health import LedgerHealth

from app.core.pagination import normalise_paging



__all__ = ["LedgerHealthRepository"]





class LedgerHealthRepository:

    model = LedgerHealth





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LedgerHealth]:

        return db.scalar(

            select(LedgerHealth).where(

                LedgerHealth.business_id == business_id, LedgerHealth.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[LedgerHealth]:

        return db.scalar(

            select(LedgerHealth).where(

                LedgerHealth.business_id == business_id, LedgerHealth.name == name

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

    ) -> tuple[Sequence[LedgerHealth], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LedgerHealth.business_id == business_id]

        if search:

            conditions.append(LedgerHealth.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(LedgerHealth).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LedgerHealth)

            .where(*conditions)

            .order_by(LedgerHealth.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: LedgerHealth) -> LedgerHealth:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: LedgerHealth) -> None:

        db.delete(row)

        db.flush()

"""Data access for BisectAccountingStatements. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bisect_accounting_statements_domain.models.bisect_accounting_statements import BisectAccountingStatements

from app.core.pagination import normalise_paging



__all__ = ["BisectAccountingStatementsRepository"]





class BisectAccountingStatementsRepository:

    model = BisectAccountingStatements





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BisectAccountingStatements]:

        return db.scalar(

            select(BisectAccountingStatements).where(

                BisectAccountingStatements.business_id == business_id, BisectAccountingStatements.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BisectAccountingStatements]:

        return db.scalar(

            select(BisectAccountingStatements).where(

                BisectAccountingStatements.business_id == business_id, BisectAccountingStatements.name == name

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

    ) -> tuple[Sequence[BisectAccountingStatements], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BisectAccountingStatements.business_id == business_id]

        if search:

            conditions.append(BisectAccountingStatements.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(BisectAccountingStatements).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BisectAccountingStatements)

            .where(*conditions)

            .order_by(BisectAccountingStatements.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: BisectAccountingStatements) -> BisectAccountingStatements:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: BisectAccountingStatements) -> None:

        db.delete(row)

        db.flush()

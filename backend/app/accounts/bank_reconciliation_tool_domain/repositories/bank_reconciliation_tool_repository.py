"""Data access for BankReconciliationTool. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_reconciliation_tool_domain.models.bank_reconciliation_tool import BankReconciliationTool

from app.core.pagination import normalise_paging



__all__ = ["BankReconciliationToolRepository"]





class BankReconciliationToolRepository:

    model = BankReconciliationTool





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BankReconciliationTool]:

        return db.scalar(

            select(BankReconciliationTool).where(

                BankReconciliationTool.business_id == business_id, BankReconciliationTool.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BankReconciliationTool]:

        return db.scalar(

            select(BankReconciliationTool).where(

                BankReconciliationTool.business_id == business_id, BankReconciliationTool.name == name

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

    ) -> tuple[Sequence[BankReconciliationTool], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BankReconciliationTool.business_id == business_id]

        if search:

            conditions.append(BankReconciliationTool.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(BankReconciliationTool).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BankReconciliationTool)

            .where(*conditions)

            .order_by(BankReconciliationTool.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: BankReconciliationTool) -> BankReconciliationTool:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: BankReconciliationTool) -> None:

        db.delete(row)

        db.flush()

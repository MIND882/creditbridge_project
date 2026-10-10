"""Data access for ProcessStatementOfAccounts. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.process_statement_of_accounts_domain.models.process_statement_of_accounts import ProcessStatementOfAccounts

from app.core.pagination import normalise_paging



__all__ = ["ProcessStatementOfAccountsRepository"]





class ProcessStatementOfAccountsRepository:

    model = ProcessStatementOfAccounts



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(ProcessStatementOfAccounts.cost_center), selectinload(ProcessStatementOfAccounts.project), selectinload(ProcessStatementOfAccounts.cc_to), selectinload(ProcessStatementOfAccounts.customers)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProcessStatementOfAccounts]:

        return db.scalar(

            select(ProcessStatementOfAccounts).where(

                ProcessStatementOfAccounts.business_id == business_id, ProcessStatementOfAccounts.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProcessStatementOfAccounts]:

        return db.scalar(

            select(ProcessStatementOfAccounts).where(

                ProcessStatementOfAccounts.business_id == business_id, ProcessStatementOfAccounts.name == name

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

    ) -> tuple[Sequence[ProcessStatementOfAccounts], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProcessStatementOfAccounts.business_id == business_id]

        if search:

            conditions.append(ProcessStatementOfAccounts.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ProcessStatementOfAccounts).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProcessStatementOfAccounts)

            .where(*conditions)

            .order_by(ProcessStatementOfAccounts.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: ProcessStatementOfAccounts) -> ProcessStatementOfAccounts:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ProcessStatementOfAccounts) -> None:

        db.delete(row)

        db.flush()

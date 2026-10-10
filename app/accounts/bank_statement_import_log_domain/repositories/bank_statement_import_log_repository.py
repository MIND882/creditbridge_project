"""Data access for BankStatementImportLog. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.bank_statement_import_log_domain.models.bank_statement_import_log import BankStatementImportLog

from app.core.pagination import normalise_paging



__all__ = ["BankStatementImportLogRepository"]





class BankStatementImportLogRepository:

    model = BankStatementImportLog



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(BankStatementImportLog.column_mapping)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BankStatementImportLog]:

        return db.scalar(

            select(BankStatementImportLog).where(

                BankStatementImportLog.business_id == business_id, BankStatementImportLog.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BankStatementImportLog]:

        return db.scalar(

            select(BankStatementImportLog).where(

                BankStatementImportLog.business_id == business_id, BankStatementImportLog.name == name

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

    ) -> tuple[Sequence[BankStatementImportLog], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BankStatementImportLog.business_id == business_id]

        if search:

            conditions.append(BankStatementImportLog.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(BankStatementImportLog).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BankStatementImportLog)

            .where(*conditions)

            .order_by(BankStatementImportLog.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: BankStatementImportLog) -> BankStatementImportLog:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: BankStatementImportLog) -> None:

        db.delete(row)

        db.flush()

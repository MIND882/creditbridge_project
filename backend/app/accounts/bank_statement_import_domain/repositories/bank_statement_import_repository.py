"""Data access for BankStatementImport. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_statement_import_domain.models.bank_statement_import import BankStatementImport

from app.core.pagination import normalise_paging



__all__ = ["BankStatementImportRepository"]





class BankStatementImportRepository:

    model = BankStatementImport





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BankStatementImport]:

        return db.scalar(

            select(BankStatementImport).where(

                BankStatementImport.business_id == business_id, BankStatementImport.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BankStatementImport]:

        return db.scalar(

            select(BankStatementImport).where(

                BankStatementImport.business_id == business_id, BankStatementImport.name == name

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

    ) -> tuple[Sequence[BankStatementImport], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BankStatementImport.business_id == business_id]

        if search:

            conditions.append(BankStatementImport.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(BankStatementImport).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BankStatementImport)

            .where(*conditions)

            .order_by(BankStatementImport.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: BankStatementImport) -> BankStatementImport:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: BankStatementImport) -> None:

        db.delete(row)

        db.flush()

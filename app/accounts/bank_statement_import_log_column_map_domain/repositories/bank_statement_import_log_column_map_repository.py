"""Data access for BankStatementImportLogColumnMap. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_statement_import_log_column_map_domain.models.bank_statement_import_log_column_map import BankStatementImportLogColumnMap

from app.core.pagination import normalise_paging



__all__ = ["BankStatementImportLogColumnMapRepository"]





class BankStatementImportLogColumnMapRepository:

    model = BankStatementImportLogColumnMap





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BankStatementImportLogColumnMap]:

        return db.scalar(

            select(BankStatementImportLogColumnMap).where(

                BankStatementImportLogColumnMap.business_id == business_id, BankStatementImportLogColumnMap.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BankStatementImportLogColumnMap], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BankStatementImportLogColumnMap.business_id == business_id]

        if parent_id is not None:

            conditions.append(BankStatementImportLogColumnMap.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BankStatementImportLogColumnMap).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BankStatementImportLogColumnMap)

            .where(*conditions)

            .order_by(BankStatementImportLogColumnMap.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



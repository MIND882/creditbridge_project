"""Data access for ProcessStatementOfAccountsCc. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_statement_of_accounts_cc_domain.models.process_statement_of_accounts_cc import ProcessStatementOfAccountsCc

from app.core.pagination import normalise_paging



__all__ = ["ProcessStatementOfAccountsCcRepository"]





class ProcessStatementOfAccountsCcRepository:

    model = ProcessStatementOfAccountsCc





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProcessStatementOfAccountsCc]:

        return db.scalar(

            select(ProcessStatementOfAccountsCc).where(

                ProcessStatementOfAccountsCc.business_id == business_id, ProcessStatementOfAccountsCc.id == row_id

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

    ) -> tuple[Sequence[ProcessStatementOfAccountsCc], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProcessStatementOfAccountsCc.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProcessStatementOfAccountsCc.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProcessStatementOfAccountsCc).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProcessStatementOfAccountsCc)

            .where(*conditions)

            .order_by(ProcessStatementOfAccountsCc.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



"""Data access for ProcessStatementOfAccountsCustomer. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_statement_of_accounts_customer_domain.models.process_statement_of_accounts_customer import ProcessStatementOfAccountsCustomer

from app.core.pagination import normalise_paging



__all__ = ["ProcessStatementOfAccountsCustomerRepository"]





class ProcessStatementOfAccountsCustomerRepository:

    model = ProcessStatementOfAccountsCustomer





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProcessStatementOfAccountsCustomer]:

        return db.scalar(

            select(ProcessStatementOfAccountsCustomer).where(

                ProcessStatementOfAccountsCustomer.business_id == business_id, ProcessStatementOfAccountsCustomer.id == row_id

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

    ) -> tuple[Sequence[ProcessStatementOfAccountsCustomer], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProcessStatementOfAccountsCustomer.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProcessStatementOfAccountsCustomer.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProcessStatementOfAccountsCustomer).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProcessStatementOfAccountsCustomer)

            .where(*conditions)

            .order_by(ProcessStatementOfAccountsCustomer.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



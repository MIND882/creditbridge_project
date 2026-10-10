"""Business logic for ProcessStatementOfAccountsCustomer.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.process_statement_of_accounts_customer_domain.models.process_statement_of_accounts_customer import ProcessStatementOfAccountsCustomer

from app.accounts.process_statement_of_accounts_customer_domain.repositories.process_statement_of_accounts_customer_repository import (

    ProcessStatementOfAccountsCustomerRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProcessStatementOfAccountsCustomerService"]





class ProcessStatementOfAccountsCustomerService:

    def __init__(self, repository: Optional[ProcessStatementOfAccountsCustomerRepository] = None) -> None:

        self.repository = repository or ProcessStatementOfAccountsCustomerRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessStatementOfAccountsCustomer:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Process Statement Of Accounts Customer", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProcessStatementOfAccountsCustomer]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProcessStatementOfAccountsCustomer].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

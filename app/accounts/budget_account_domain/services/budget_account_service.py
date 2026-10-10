"""Business logic for BudgetAccount.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.budget_account_domain.models.budget_account import BudgetAccount

from app.accounts.budget_account_domain.repositories.budget_account_repository import (

    BudgetAccountRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BudgetAccountService"]





class BudgetAccountService:

    def __init__(self, repository: Optional[BudgetAccountRepository] = None) -> None:

        self.repository = repository or BudgetAccountRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BudgetAccount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Budget Account", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BudgetAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BudgetAccount].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

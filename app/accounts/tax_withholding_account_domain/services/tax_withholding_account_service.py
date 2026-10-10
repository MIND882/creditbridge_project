"""Read-only service for TaxWithholdingAccount; writes go through the parent doctype."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.tax_withholding_account_domain.models.tax_withholding_account import TaxWithholdingAccount

from app.accounts.tax_withholding_account_domain.repositories.tax_withholding_account_repository import TaxWithholdingAccountRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["TaxWithholdingAccountService"]





class TaxWithholdingAccountService:

    def __init__(self, repository: Optional[TaxWithholdingAccountRepository] = None) -> None:

        self.repository = repository or TaxWithholdingAccountRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> TaxWithholdingAccount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("TaxWithholdingAccount", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[TaxWithholdingAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[TaxWithholdingAccount].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

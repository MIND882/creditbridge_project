"""Business logic for ExchangeRateRevaluationAccount.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.exchange_rate_revaluation_account_domain.models.exchange_rate_revaluation_account import ExchangeRateRevaluationAccount

from app.accounts.exchange_rate_revaluation_account_domain.repositories.exchange_rate_revaluation_account_repository import (

    ExchangeRateRevaluationAccountRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ExchangeRateRevaluationAccountService"]





class ExchangeRateRevaluationAccountService:

    def __init__(self, repository: Optional[ExchangeRateRevaluationAccountRepository] = None) -> None:

        self.repository = repository or ExchangeRateRevaluationAccountRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ExchangeRateRevaluationAccount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Exchange Rate Revaluation Account", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ExchangeRateRevaluationAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ExchangeRateRevaluationAccount].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

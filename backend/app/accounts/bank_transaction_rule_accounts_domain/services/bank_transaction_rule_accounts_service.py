"""Read-only service for BankTransactionRuleAccount; writes go through BankTransactionRule."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_transaction_rule_accounts_domain.models.bank_transaction_rule_accounts import BankTransactionRuleAccount

from app.accounts.bank_transaction_rule_accounts_domain.repositories.bank_transaction_rule_accounts_repository import BankTransactionRuleAccountRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankTransactionRuleAccountService"]





class BankTransactionRuleAccountService:

    def __init__(self, repository: Optional[BankTransactionRuleAccountRepository] = None) -> None:

        self.repository = repository or BankTransactionRuleAccountRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> BankTransactionRuleAccount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BankTransactionRuleAccount", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[BankTransactionRuleAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankTransactionRuleAccount].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

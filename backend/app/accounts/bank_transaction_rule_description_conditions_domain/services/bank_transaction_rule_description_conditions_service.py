"""Read-only service for BankTransactionRuleDescriptionCondition; writes go through BankTransactionRule."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_transaction_rule_description_conditions_domain.models.bank_transaction_rule_description_conditions import BankTransactionRuleDescriptionCondition

from app.accounts.bank_transaction_rule_description_conditions_domain.repositories.bank_transaction_rule_description_conditions_repository import BankTransactionRuleDescriptionConditionRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankTransactionRuleDescriptionConditionService"]





class BankTransactionRuleDescriptionConditionService:

    def __init__(self, repository: Optional[BankTransactionRuleDescriptionConditionRepository] = None) -> None:

        self.repository = repository or BankTransactionRuleDescriptionConditionRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> BankTransactionRuleDescriptionCondition:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BankTransactionRuleDescriptionCondition", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[BankTransactionRuleDescriptionCondition]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankTransactionRuleDescriptionCondition].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

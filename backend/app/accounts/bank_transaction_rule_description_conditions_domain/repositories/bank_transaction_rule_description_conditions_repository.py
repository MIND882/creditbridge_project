"""Data access for BankTransactionRuleDescriptionCondition. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_transaction_rule_description_conditions_domain.models.bank_transaction_rule_description_conditions import BankTransactionRuleDescriptionCondition

from app.core.pagination import normalise_paging



__all__ = ["BankTransactionRuleDescriptionConditionRepository"]





class BankTransactionRuleDescriptionConditionRepository:

    model = BankTransactionRuleDescriptionCondition



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BankTransactionRuleDescriptionCondition]:

        return db.scalar(

            select(BankTransactionRuleDescriptionCondition).where(BankTransactionRuleDescriptionCondition.business_id == business_id, BankTransactionRuleDescriptionCondition.id == row_id)

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BankTransactionRuleDescriptionCondition], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [BankTransactionRuleDescriptionCondition.business_id == business_id]

        if parent_id is not None:

            conditions.append(BankTransactionRuleDescriptionCondition.parent_id == parent_id)



        total = int(db.scalar(select(func.count()).select_from(BankTransactionRuleDescriptionCondition).where(*conditions)) or 0)

        rows = db.scalars(

            select(BankTransactionRuleDescriptionCondition).where(*conditions).order_by(BankTransactionRuleDescriptionCondition.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total

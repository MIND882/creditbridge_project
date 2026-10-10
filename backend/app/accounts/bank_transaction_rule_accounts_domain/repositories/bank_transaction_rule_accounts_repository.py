"""Data access for BankTransactionRuleAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_transaction_rule_accounts_domain.models.bank_transaction_rule_accounts import BankTransactionRuleAccount

from app.core.pagination import normalise_paging



__all__ = ["BankTransactionRuleAccountRepository"]





class BankTransactionRuleAccountRepository:

    model = BankTransactionRuleAccount



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BankTransactionRuleAccount]:

        return db.scalar(

            select(BankTransactionRuleAccount).where(BankTransactionRuleAccount.business_id == business_id, BankTransactionRuleAccount.id == row_id)

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BankTransactionRuleAccount], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [BankTransactionRuleAccount.business_id == business_id]

        if parent_id is not None:

            conditions.append(BankTransactionRuleAccount.parent_id == parent_id)



        total = int(db.scalar(select(func.count()).select_from(BankTransactionRuleAccount).where(*conditions)) or 0)

        rows = db.scalars(

            select(BankTransactionRuleAccount).where(*conditions).order_by(BankTransactionRuleAccount.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total

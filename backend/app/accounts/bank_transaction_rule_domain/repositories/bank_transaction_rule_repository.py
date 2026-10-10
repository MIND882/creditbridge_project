"""Data access for Bank Transaction Rule. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.bank_transaction_rule_domain.models.bank_transaction_rule import (

    BankTransactionRule,

)

from app.core.pagination import normalise_paging



__all__ = ["BankTransactionRuleRepository"]





class BankTransactionRuleRepository:

    model = BankTransactionRule



    @staticmethod

    def _eager() -> tuple:

        """

        Loader options, built on demand.



        Deliberately NOT a class attribute: a class body runs at import time,

        and ``selectinload()`` forces SQLAlchemy to configure every mapper right

        then. That breaks conftest collection, where models are imported in a

        specific order and a relationship target may not exist yet.

        """

        return (

            selectinload(BankTransactionRule.description_rules),

            selectinload(BankTransactionRule.accounts),

        )



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, rule_id: uuid.UUID

    ) -> Optional[BankTransactionRule]:

        return db.scalar(

            select(BankTransactionRule)

            .options(*self._eager())

            .where(

                BankTransactionRule.business_id == business_id,

                BankTransactionRule.id == rule_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, rule_name: str, *, exclude_id: Optional[uuid.UUID] = None

    ) -> Optional[BankTransactionRule]:

        conditions = [

            BankTransactionRule.business_id == business_id,

            BankTransactionRule.rule_name == rule_name,

        ]

        if exclude_id is not None:

            conditions.append(BankTransactionRule.id != exclude_id)

        return db.scalar(select(BankTransactionRule).where(*conditions))



    def highest_priority(self, db: Session, business_id: uuid.UUID) -> int:

        """``before_insert``: the highest priority so far, 0 when there are none."""

        return int(

            db.scalar(

                select(func.max(BankTransactionRule.priority)).where(

                    BankTransactionRule.business_id == business_id

                )

            )

            or 0

        )



    def list_by_priority(self, db: Session, business_id: uuid.UUID) -> list[BankTransactionRule]:

        """Evaluation order for rule matching."""

        return list(

            db.scalars(

                select(BankTransactionRule)

                .options(*self._eager())

                .where(BankTransactionRule.business_id == business_id)

                .order_by(BankTransactionRule.priority.asc())

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[BankTransactionRule], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [BankTransactionRule.business_id == business_id]

        if search:

            pattern = f"%{search}%"

            conditions.append(

                BankTransactionRule.rule_name.ilike(pattern)

                | BankTransactionRule.rule_description.ilike(pattern)

            )



        total = int(

            db.scalar(select(func.count()).select_from(BankTransactionRule).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(BankTransactionRule)

            .options(*self._eager())

            .where(*conditions)

            .order_by(BankTransactionRule.priority.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, rule: BankTransactionRule) -> BankTransactionRule:

        db.add(rule)

        db.flush()

        return rule



    def delete(self, db: Session, rule: BankTransactionRule) -> None:

        db.delete(rule)

        db.flush()

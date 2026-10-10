"""

Data access for Bank Account Balance.



A child table: reads are by parent; writes go through the Bank Account service so

``idx`` ordering stays consistent.

"""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_account_balance_domain.models.bank_account_balance import BankAccountBalance

from app.core.pagination import normalise_paging



__all__ = ["BankAccountBalanceRepository"]





class BankAccountBalanceRepository:

    model = BankAccountBalance



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[BankAccountBalance]:

        return db.scalar(

            select(BankAccountBalance).where(

                BankAccountBalance.business_id == business_id, BankAccountBalance.id == row_id

            )

        )



    def list_by_parent(

        self, db: Session, business_id: uuid.UUID, parent_id: uuid.UUID

    ) -> list[BankAccountBalance]:

        return list(

            db.scalars(

                select(BankAccountBalance)

                .where(

                    BankAccountBalance.business_id == business_id,

                    BankAccountBalance.parent_id == parent_id,

                )

                .order_by(BankAccountBalance.idx.asc())

            )

        )



    def list(

        self, db: Session, business_id: uuid.UUID, *, offset: int = 0, limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BankAccountBalance], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BankAccountBalance.business_id == business_id]

        if parent_id is not None:

            conditions.append(BankAccountBalance.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BankAccountBalance).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(BankAccountBalance).where(*conditions).order_by(BankAccountBalance.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: BankAccountBalance) -> BankAccountBalance:

        db.add(row)

        db.flush()

        return row

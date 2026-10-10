"""Data access for AccountClosingBalance. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.account_closing_balance_domain.models.account_closing_balance import AccountClosingBalance

from app.core.pagination import normalise_paging



__all__ = ["AccountClosingBalanceRepository"]





class AccountClosingBalanceRepository:

    model = AccountClosingBalance





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[AccountClosingBalance]:

        return db.scalar(

            select(AccountClosingBalance).where(

                AccountClosingBalance.business_id == business_id, AccountClosingBalance.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[AccountClosingBalance]:

        return db.scalar(

            select(AccountClosingBalance).where(

                AccountClosingBalance.business_id == business_id, AccountClosingBalance.name == name

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

        include_cancelled: bool = False,

    ) -> tuple[Sequence[AccountClosingBalance], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [AccountClosingBalance.business_id == business_id]

        if not include_cancelled:

            conditions.append(AccountClosingBalance.docstatus != 2)

        if search:

            conditions.append(AccountClosingBalance.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(AccountClosingBalance).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(AccountClosingBalance)

            .where(*conditions)

            .order_by(AccountClosingBalance.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: AccountClosingBalance) -> AccountClosingBalance:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: AccountClosingBalance) -> None:

        db.delete(row)

        db.flush()

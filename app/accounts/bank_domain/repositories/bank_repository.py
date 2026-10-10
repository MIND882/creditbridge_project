"""Data access for Bank. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.bank_domain.models.bank import Bank

from app.core.pagination import normalise_paging



__all__ = ["BankRepository"]





class BankRepository:

    model = Bank



    def get_by_id(self, db: Session, business_id: uuid.UUID, bank_id: uuid.UUID) -> Optional[Bank]:

        return db.scalar(

            select(Bank)

            .options(selectinload(Bank.bank_transaction_mapping))

            .where(Bank.business_id == business_id, Bank.id == bank_id)

        )



    def get_by_name(self, db: Session, business_id: uuid.UUID, bank_name: str) -> Optional[Bank]:

        return db.scalar(

            select(Bank)

            .options(selectinload(Bank.bank_transaction_mapping))

            .where(Bank.business_id == business_id, Bank.bank_name == bank_name)

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[Bank], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [Bank.business_id == business_id]

        if search:

            conditions.append(

                Bank.bank_name.ilike(f"%{search}%") | Bank.name.ilike(f"%{search}%")

            )



        total = int(db.scalar(select(func.count()).select_from(Bank).where(*conditions)) or 0)

        rows = db.scalars(

            select(Bank)

            .options(selectinload(Bank.bank_transaction_mapping))

            .where(*conditions)

            .order_by(Bank.bank_name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, bank: Bank) -> Bank:

        db.add(bank)

        db.flush()

        return bank



    def delete(self, db: Session, bank: Bank) -> None:

        db.delete(bank)

        db.flush()

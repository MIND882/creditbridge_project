"""Data access for Bank Account Type. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_account_type_domain.models.bank_account_type import BankAccountType

from app.core.pagination import normalise_paging



__all__ = ["BankAccountTypeRepository"]





class BankAccountTypeRepository:

    model = BankAccountType



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[BankAccountType]:

        return db.scalar(

            select(BankAccountType).where(

                BankAccountType.business_id == business_id, BankAccountType.id == row_id

            )

        )



    def get_by_name(self, db: Session, business_id: uuid.UUID, name: str) -> Optional[BankAccountType]:

        return db.scalar(

            select(BankAccountType).where(

                BankAccountType.business_id == business_id, BankAccountType.account_type == name

            )

        )



    def list(

        self, db: Session, business_id: uuid.UUID, *, offset: int = 0, limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[BankAccountType], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BankAccountType.business_id == business_id]

        if search:

            conditions.append(BankAccountType.account_type.ilike(f"%{search}%"))



        total = int(db.scalar(select(func.count()).select_from(BankAccountType).where(*conditions)) or 0)

        rows = db.scalars(

            select(BankAccountType).where(*conditions).order_by(BankAccountType.account_type.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: BankAccountType) -> BankAccountType:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: BankAccountType) -> None:

        db.delete(row)

        db.flush()

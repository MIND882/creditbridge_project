"""Data access for Bank Account Subtype. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_account_subtype_domain.models.bank_account_subtype import BankAccountSubtype

from app.core.pagination import normalise_paging



__all__ = ["BankAccountSubtypeRepository"]





class BankAccountSubtypeRepository:

    model = BankAccountSubtype



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[BankAccountSubtype]:

        return db.scalar(

            select(BankAccountSubtype).where(

                BankAccountSubtype.business_id == business_id, BankAccountSubtype.id == row_id

            )

        )



    def get_by_name(self, db: Session, business_id: uuid.UUID, name: str) -> Optional[BankAccountSubtype]:

        return db.scalar(

            select(BankAccountSubtype).where(

                BankAccountSubtype.business_id == business_id, BankAccountSubtype.account_subtype == name

            )

        )



    def list(

        self, db: Session, business_id: uuid.UUID, *, offset: int = 0, limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[BankAccountSubtype], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BankAccountSubtype.business_id == business_id]

        if search:

            conditions.append(BankAccountSubtype.account_subtype.ilike(f"%{search}%"))



        total = int(db.scalar(select(func.count()).select_from(BankAccountSubtype).where(*conditions)) or 0)

        rows = db.scalars(

            select(BankAccountSubtype).where(*conditions).order_by(BankAccountSubtype.account_subtype.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: BankAccountSubtype) -> BankAccountSubtype:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: BankAccountSubtype) -> None:

        db.delete(row)

        db.flush()

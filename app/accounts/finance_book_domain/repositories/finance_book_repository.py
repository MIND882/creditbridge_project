"""Data access for Finance Book. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.finance_book_domain.models.finance_book import FinanceBook

from app.core.pagination import normalise_paging



__all__ = ["FinanceBookRepository"]





class FinanceBookRepository:

    model = FinanceBook



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[FinanceBook]:

        return db.scalar(

            select(FinanceBook).where(

                FinanceBook.business_id == business_id, FinanceBook.id == row_id

            )

        )



    def get_by_name(self, db: Session, business_id: uuid.UUID, name: str) -> Optional[FinanceBook]:

        return db.scalar(

            select(FinanceBook).where(

                FinanceBook.business_id == business_id, FinanceBook.finance_book_name == name

            )

        )



    def list(

        self, db: Session, business_id: uuid.UUID, *, offset: int = 0, limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[FinanceBook], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [FinanceBook.business_id == business_id]

        if search:

            conditions.append(FinanceBook.finance_book_name.ilike(f"%{search}%"))



        total = int(db.scalar(select(func.count()).select_from(FinanceBook).where(*conditions)) or 0)

        rows = db.scalars(

            select(FinanceBook).where(*conditions).order_by(FinanceBook.finance_book_name.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: FinanceBook) -> FinanceBook:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: FinanceBook) -> None:

        db.delete(row)

        db.flush()

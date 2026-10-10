"""Data access for Bank Transaction. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.bank_transaction_domain.models.bank_transaction import (

    BankTransaction,

    BankTransactionStatus,

)

from app.core.pagination import normalise_paging



__all__ = ["BankTransactionRepository"]





class BankTransactionRepository:

    model = BankTransaction



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, transaction_id: uuid.UUID

    ) -> Optional[BankTransaction]:

        return db.scalar(

            select(BankTransaction)

            .options(selectinload(BankTransaction.payment_entries))

            .where(

                BankTransaction.business_id == business_id,

                BankTransaction.id == transaction_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BankTransaction]:

        return db.scalar(

            select(BankTransaction).where(

                BankTransaction.business_id == business_id, BankTransaction.name == name

            )

        )



    def next_name(self, db: Session, business_id: uuid.UUID, on: date) -> str:

        """``ACC-BTN-.YYYY.-#####``, counter scoped per tenant and year."""

        start, end = date(on.year, 1, 1), date(on.year, 12, 31)

        count = int(

            db.scalar(

                select(func.count())

                .select_from(BankTransaction)

                .where(

                    BankTransaction.business_id == business_id,

                    BankTransaction.created_at >= start,

                    BankTransaction.created_at <= end,

                )

            )

            or 0

        )

        return f"ACC-BTN-{on.year}-{count + 1:05d}"



    def list_matching_rule(

        self, db: Session, business_id: uuid.UUID, rule_id: uuid.UUID

    ) -> list[BankTransaction]:

        """Transactions currently attributed to a rule (used when a rule is deleted)."""

        return list(

            db.scalars(

                select(BankTransaction).where(

                    BankTransaction.business_id == business_id,

                    BankTransaction.matched_transaction_rule_id == rule_id,

                )

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        status: Optional[BankTransactionStatus] = None,

        bank_account_id: Optional[uuid.UUID] = None,

        from_date: Optional[date] = None,

        to_date: Optional[date] = None,

        search: Optional[str] = None,

        docstatus: Optional[int] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[BankTransaction], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [BankTransaction.business_id == business_id]

        if status is not None:

            conditions.append(BankTransaction.status == status)

        if bank_account_id is not None:

            conditions.append(BankTransaction.bank_account_id == bank_account_id)

        if from_date is not None:

            conditions.append(BankTransaction.date >= from_date)

        if to_date is not None:

            conditions.append(BankTransaction.date <= to_date)

        if search:

            pattern = f"%{search}%"

            conditions.append(

                BankTransaction.description.ilike(pattern)

                | BankTransaction.reference_number.ilike(pattern)

                | BankTransaction.party.ilike(pattern)

                | BankTransaction.name.ilike(pattern)

            )

        if docstatus is not None:

            conditions.append(BankTransaction.docstatus == docstatus)

        elif not include_cancelled:

            # Mirrors ERPNext's ubiquitous `docstatus != 2`.

            conditions.append(BankTransaction.docstatus != 2)



        total = int(

            db.scalar(select(func.count()).select_from(BankTransaction).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(BankTransaction)

            .options(selectinload(BankTransaction.payment_entries))

            .where(*conditions)

            .order_by(BankTransaction.date.desc(), BankTransaction.name.desc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, transaction: BankTransaction) -> BankTransaction:

        db.add(transaction)

        db.flush()

        return transaction



    def delete(self, db: Session, transaction: BankTransaction) -> None:

        db.delete(transaction)

        db.flush()

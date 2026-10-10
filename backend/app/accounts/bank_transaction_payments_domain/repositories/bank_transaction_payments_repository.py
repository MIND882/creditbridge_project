"""Data access for BankTransactionPayment. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_transaction_payments_domain.models.bank_transaction_payments import BankTransactionPayment

from app.core.pagination import normalise_paging



__all__ = ["BankTransactionPaymentRepository"]





class BankTransactionPaymentRepository:

    model = BankTransactionPayment



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BankTransactionPayment]:

        return db.scalar(

            select(BankTransactionPayment).where(BankTransactionPayment.business_id == business_id, BankTransactionPayment.id == row_id)

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BankTransactionPayment], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [BankTransactionPayment.business_id == business_id]

        if parent_id is not None:

            conditions.append(BankTransactionPayment.parent_id == parent_id)



        total = int(db.scalar(select(func.count()).select_from(BankTransactionPayment).where(*conditions)) or 0)

        rows = db.scalars(

            select(BankTransactionPayment).where(*conditions).order_by(BankTransactionPayment.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total

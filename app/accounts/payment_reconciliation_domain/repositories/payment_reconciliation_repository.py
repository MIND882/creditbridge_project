"""Data access for PaymentReconciliation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.payment_reconciliation_domain.models.payment_reconciliation import PaymentReconciliation

from app.core.pagination import normalise_paging



__all__ = ["PaymentReconciliationRepository"]





class PaymentReconciliationRepository:

    model = PaymentReconciliation



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(PaymentReconciliation.payments), selectinload(PaymentReconciliation.invoices), selectinload(PaymentReconciliation.allocation)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PaymentReconciliation]:

        return db.scalar(

            select(PaymentReconciliation).where(

                PaymentReconciliation.business_id == business_id, PaymentReconciliation.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PaymentReconciliation]:

        return db.scalar(

            select(PaymentReconciliation).where(

                PaymentReconciliation.business_id == business_id, PaymentReconciliation.name == name

            ).options(*self._options())

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[PaymentReconciliation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentReconciliation.business_id == business_id]

        if search:

            conditions.append(PaymentReconciliation.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PaymentReconciliation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PaymentReconciliation)

            .where(*conditions)

            .order_by(PaymentReconciliation.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: PaymentReconciliation) -> PaymentReconciliation:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PaymentReconciliation) -> None:

        db.delete(row)

        db.flush()

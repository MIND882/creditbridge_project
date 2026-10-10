"""Data access for PaymentOrder. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.payment_order_domain.models.payment_order import PaymentOrder

from app.core.pagination import normalise_paging



__all__ = ["PaymentOrderRepository"]





class PaymentOrderRepository:

    model = PaymentOrder



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(PaymentOrder.references)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PaymentOrder]:

        return db.scalar(

            select(PaymentOrder).where(

                PaymentOrder.business_id == business_id, PaymentOrder.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PaymentOrder]:

        return db.scalar(

            select(PaymentOrder).where(

                PaymentOrder.business_id == business_id, PaymentOrder.name == name

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

        include_cancelled: bool = False,

    ) -> tuple[Sequence[PaymentOrder], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentOrder.business_id == business_id]

        if not include_cancelled:

            conditions.append(PaymentOrder.docstatus != 2)

        if search:

            conditions.append(PaymentOrder.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PaymentOrder).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PaymentOrder)

            .where(*conditions)

            .order_by(PaymentOrder.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: PaymentOrder) -> PaymentOrder:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PaymentOrder) -> None:

        db.delete(row)

        db.flush()

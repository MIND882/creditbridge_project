"""Data access for PaymentRequest. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.payment_request_domain.models.payment_request import PaymentRequest

from app.core.pagination import normalise_paging



__all__ = ["PaymentRequestRepository"]





class PaymentRequestRepository:

    model = PaymentRequest



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(PaymentRequest.subscription_plans), selectinload(PaymentRequest.payment_reference)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PaymentRequest]:

        return db.scalar(

            select(PaymentRequest).where(

                PaymentRequest.business_id == business_id, PaymentRequest.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PaymentRequest]:

        return db.scalar(

            select(PaymentRequest).where(

                PaymentRequest.business_id == business_id, PaymentRequest.name == name

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

    ) -> tuple[Sequence[PaymentRequest], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentRequest.business_id == business_id]

        if not include_cancelled:

            conditions.append(PaymentRequest.docstatus != 2)

        if search:

            conditions.append(PaymentRequest.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PaymentRequest).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PaymentRequest)

            .where(*conditions)

            .order_by(PaymentRequest.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: PaymentRequest) -> PaymentRequest:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PaymentRequest) -> None:

        db.delete(row)

        db.flush()

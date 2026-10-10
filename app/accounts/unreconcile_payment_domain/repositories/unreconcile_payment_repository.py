"""Data access for UnreconcilePayment. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.unreconcile_payment_domain.models.unreconcile_payment import UnreconcilePayment

from app.core.pagination import normalise_paging



__all__ = ["UnreconcilePaymentRepository"]





class UnreconcilePaymentRepository:

    model = UnreconcilePayment



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(UnreconcilePayment.allocations)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[UnreconcilePayment]:

        return db.scalar(

            select(UnreconcilePayment).where(

                UnreconcilePayment.business_id == business_id, UnreconcilePayment.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[UnreconcilePayment]:

        return db.scalar(

            select(UnreconcilePayment).where(

                UnreconcilePayment.business_id == business_id, UnreconcilePayment.name == name

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

    ) -> tuple[Sequence[UnreconcilePayment], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [UnreconcilePayment.business_id == business_id]

        if not include_cancelled:

            conditions.append(UnreconcilePayment.docstatus != 2)

        if search:

            conditions.append(UnreconcilePayment.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(UnreconcilePayment).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(UnreconcilePayment)

            .where(*conditions)

            .order_by(UnreconcilePayment.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: UnreconcilePayment) -> UnreconcilePayment:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: UnreconcilePayment) -> None:

        db.delete(row)

        db.flush()

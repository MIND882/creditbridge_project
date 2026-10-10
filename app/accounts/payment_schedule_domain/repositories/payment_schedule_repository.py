"""Data access for Payment Schedule. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_schedule_domain.models.payment_schedule import PaymentSchedule

from app.core.pagination import normalise_paging



__all__ = ["PaymentScheduleRepository"]





class PaymentScheduleRepository:

    model = PaymentSchedule



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PaymentSchedule]:

        return db.scalar(

            select(PaymentSchedule).where(

                PaymentSchedule.business_id == business_id, PaymentSchedule.id == row_id

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        payment_term_id: Optional[uuid.UUID] = None,

        from_date: Optional[date] = None,

        to_date: Optional[date] = None,

    ) -> tuple[Sequence[PaymentSchedule], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentSchedule.business_id == business_id]

        if payment_term_id is not None:

            conditions.append(PaymentSchedule.payment_term_id == payment_term_id)

        if from_date is not None:

            conditions.append(PaymentSchedule.due_date >= from_date)

        if to_date is not None:

            conditions.append(PaymentSchedule.due_date <= to_date)



        total = int(

            db.scalar(select(func.count()).select_from(PaymentSchedule).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(PaymentSchedule)

            .where(*conditions)

            .order_by(PaymentSchedule.due_date.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

"""Data access for OverduePayment. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.overdue_payment_domain.models.overdue_payment import OverduePayment

from app.core.pagination import normalise_paging



__all__ = ["OverduePaymentRepository"]





class OverduePaymentRepository:

    model = OverduePayment





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[OverduePayment]:

        return db.scalar(

            select(OverduePayment).where(

                OverduePayment.business_id == business_id, OverduePayment.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[OverduePayment], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [OverduePayment.business_id == business_id]

        if parent_id is not None:

            conditions.append(OverduePayment.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(OverduePayment).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(OverduePayment)

            .where(*conditions)

            .order_by(OverduePayment.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



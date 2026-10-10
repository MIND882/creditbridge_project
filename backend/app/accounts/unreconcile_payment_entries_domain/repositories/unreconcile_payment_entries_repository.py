"""Data access for UnreconcilePaymentEntries. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.unreconcile_payment_entries_domain.models.unreconcile_payment_entries import UnreconcilePaymentEntries

from app.core.pagination import normalise_paging



__all__ = ["UnreconcilePaymentEntriesRepository"]





class UnreconcilePaymentEntriesRepository:

    model = UnreconcilePaymentEntries





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[UnreconcilePaymentEntries]:

        return db.scalar(

            select(UnreconcilePaymentEntries).where(

                UnreconcilePaymentEntries.business_id == business_id, UnreconcilePaymentEntries.id == row_id

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

    ) -> tuple[Sequence[UnreconcilePaymentEntries], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [UnreconcilePaymentEntries.business_id == business_id]

        if parent_id is not None:

            conditions.append(UnreconcilePaymentEntries.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(UnreconcilePaymentEntries).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(UnreconcilePaymentEntries)

            .where(*conditions)

            .order_by(UnreconcilePaymentEntries.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



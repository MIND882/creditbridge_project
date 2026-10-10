"""Data access for PaymentReconciliationAllocation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_reconciliation_allocation_domain.models.payment_reconciliation_allocation import PaymentReconciliationAllocation

from app.core.pagination import normalise_paging



__all__ = ["PaymentReconciliationAllocationRepository"]





class PaymentReconciliationAllocationRepository:

    model = PaymentReconciliationAllocation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PaymentReconciliationAllocation]:

        return db.scalar(

            select(PaymentReconciliationAllocation).where(

                PaymentReconciliationAllocation.business_id == business_id, PaymentReconciliationAllocation.id == row_id

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

    ) -> tuple[Sequence[PaymentReconciliationAllocation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentReconciliationAllocation.business_id == business_id]

        if parent_id is not None:

            conditions.append(PaymentReconciliationAllocation.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PaymentReconciliationAllocation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PaymentReconciliationAllocation)

            .where(*conditions)

            .order_by(PaymentReconciliationAllocation.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



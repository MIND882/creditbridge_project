"""Data access for ProcessPaymentReconciliationLogAllocations. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_payment_reconciliation_log_allocations_domain.models.process_payment_reconciliation_log_allocations import ProcessPaymentReconciliationLogAllocations

from app.core.pagination import normalise_paging



__all__ = ["ProcessPaymentReconciliationLogAllocationsRepository"]





class ProcessPaymentReconciliationLogAllocationsRepository:

    model = ProcessPaymentReconciliationLogAllocations





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProcessPaymentReconciliationLogAllocations]:

        return db.scalar(

            select(ProcessPaymentReconciliationLogAllocations).where(

                ProcessPaymentReconciliationLogAllocations.business_id == business_id, ProcessPaymentReconciliationLogAllocations.id == row_id

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

    ) -> tuple[Sequence[ProcessPaymentReconciliationLogAllocations], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProcessPaymentReconciliationLogAllocations.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProcessPaymentReconciliationLogAllocations.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProcessPaymentReconciliationLogAllocations).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProcessPaymentReconciliationLogAllocations)

            .where(*conditions)

            .order_by(ProcessPaymentReconciliationLogAllocations.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



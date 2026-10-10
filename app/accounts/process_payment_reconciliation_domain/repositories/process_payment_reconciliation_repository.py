"""Data access for ProcessPaymentReconciliation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_payment_reconciliation_domain.models.process_payment_reconciliation import ProcessPaymentReconciliation

from app.core.pagination import normalise_paging



__all__ = ["ProcessPaymentReconciliationRepository"]





class ProcessPaymentReconciliationRepository:

    model = ProcessPaymentReconciliation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProcessPaymentReconciliation]:

        return db.scalar(

            select(ProcessPaymentReconciliation).where(

                ProcessPaymentReconciliation.business_id == business_id, ProcessPaymentReconciliation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProcessPaymentReconciliation]:

        return db.scalar(

            select(ProcessPaymentReconciliation).where(

                ProcessPaymentReconciliation.business_id == business_id, ProcessPaymentReconciliation.name == name

            )

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

    ) -> tuple[Sequence[ProcessPaymentReconciliation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProcessPaymentReconciliation.business_id == business_id]

        if not include_cancelled:

            conditions.append(ProcessPaymentReconciliation.docstatus != 2)

        if search:

            conditions.append(ProcessPaymentReconciliation.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ProcessPaymentReconciliation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProcessPaymentReconciliation)

            .where(*conditions)

            .order_by(ProcessPaymentReconciliation.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ProcessPaymentReconciliation) -> ProcessPaymentReconciliation:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ProcessPaymentReconciliation) -> None:

        db.delete(row)

        db.flush()

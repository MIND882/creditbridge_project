"""Data access for ProcessPaymentReconciliationLog. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.process_payment_reconciliation_log_domain.models.process_payment_reconciliation_log import ProcessPaymentReconciliationLog

from app.core.pagination import normalise_paging



__all__ = ["ProcessPaymentReconciliationLogRepository"]





class ProcessPaymentReconciliationLogRepository:

    model = ProcessPaymentReconciliationLog



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(ProcessPaymentReconciliationLog.allocations)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProcessPaymentReconciliationLog]:

        return db.scalar(

            select(ProcessPaymentReconciliationLog).where(

                ProcessPaymentReconciliationLog.business_id == business_id, ProcessPaymentReconciliationLog.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProcessPaymentReconciliationLog]:

        return db.scalar(

            select(ProcessPaymentReconciliationLog).where(

                ProcessPaymentReconciliationLog.business_id == business_id, ProcessPaymentReconciliationLog.name == name

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

    ) -> tuple[Sequence[ProcessPaymentReconciliationLog], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProcessPaymentReconciliationLog.business_id == business_id]

        if search:

            conditions.append(ProcessPaymentReconciliationLog.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ProcessPaymentReconciliationLog).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProcessPaymentReconciliationLog)

            .where(*conditions)

            .order_by(ProcessPaymentReconciliationLog.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: ProcessPaymentReconciliationLog) -> ProcessPaymentReconciliationLog:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ProcessPaymentReconciliationLog) -> None:

        db.delete(row)

        db.flush()

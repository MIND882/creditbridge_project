"""Data access for ProcessDeferredAccounting. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_deferred_accounting_domain.models.process_deferred_accounting import ProcessDeferredAccounting

from app.core.pagination import normalise_paging



__all__ = ["ProcessDeferredAccountingRepository"]





class ProcessDeferredAccountingRepository:

    model = ProcessDeferredAccounting





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProcessDeferredAccounting]:

        return db.scalar(

            select(ProcessDeferredAccounting).where(

                ProcessDeferredAccounting.business_id == business_id, ProcessDeferredAccounting.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProcessDeferredAccounting]:

        return db.scalar(

            select(ProcessDeferredAccounting).where(

                ProcessDeferredAccounting.business_id == business_id, ProcessDeferredAccounting.name == name

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

    ) -> tuple[Sequence[ProcessDeferredAccounting], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProcessDeferredAccounting.business_id == business_id]

        if not include_cancelled:

            conditions.append(ProcessDeferredAccounting.docstatus != 2)

        if search:

            conditions.append(ProcessDeferredAccounting.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ProcessDeferredAccounting).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProcessDeferredAccounting)

            .where(*conditions)

            .order_by(ProcessDeferredAccounting.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ProcessDeferredAccounting) -> ProcessDeferredAccounting:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ProcessDeferredAccounting) -> None:

        db.delete(row)

        db.flush()

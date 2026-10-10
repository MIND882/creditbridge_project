"""Data access for LedgerHealthMonitorCompany. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.ledger_health_monitor_company_domain.models.ledger_health_monitor_company import LedgerHealthMonitorCompany

from app.core.pagination import normalise_paging



__all__ = ["LedgerHealthMonitorCompanyRepository"]





class LedgerHealthMonitorCompanyRepository:

    model = LedgerHealthMonitorCompany





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LedgerHealthMonitorCompany]:

        return db.scalar(

            select(LedgerHealthMonitorCompany).where(

                LedgerHealthMonitorCompany.business_id == business_id, LedgerHealthMonitorCompany.id == row_id

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

    ) -> tuple[Sequence[LedgerHealthMonitorCompany], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LedgerHealthMonitorCompany.business_id == business_id]

        if parent_id is not None:

            conditions.append(LedgerHealthMonitorCompany.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(LedgerHealthMonitorCompany).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LedgerHealthMonitorCompany)

            .where(*conditions)

            .order_by(LedgerHealthMonitorCompany.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



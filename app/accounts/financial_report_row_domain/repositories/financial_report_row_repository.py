"""Data access for FinancialReportRow. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.financial_report_row_domain.models.financial_report_row import FinancialReportRow

from app.core.pagination import normalise_paging



__all__ = ["FinancialReportRowRepository"]





class FinancialReportRowRepository:

    model = FinancialReportRow





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[FinancialReportRow]:

        return db.scalar(

            select(FinancialReportRow).where(

                FinancialReportRow.business_id == business_id, FinancialReportRow.id == row_id

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

    ) -> tuple[Sequence[FinancialReportRow], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [FinancialReportRow.business_id == business_id]

        if parent_id is not None:

            conditions.append(FinancialReportRow.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(FinancialReportRow).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(FinancialReportRow)

            .where(*conditions)

            .order_by(FinancialReportRow.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



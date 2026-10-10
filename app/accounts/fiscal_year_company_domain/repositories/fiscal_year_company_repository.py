"""Data access for FiscalYearCompany. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.fiscal_year_company_domain.models.fiscal_year_company import FiscalYearCompany

from app.core.pagination import normalise_paging



__all__ = ["FiscalYearCompanyRepository"]





class FiscalYearCompanyRepository:

    model = FiscalYearCompany



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[FiscalYearCompany]:

        return db.scalar(

            select(FiscalYearCompany).where(

                FiscalYearCompany.business_id == business_id,

                FiscalYearCompany.id == row_id,

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

    ) -> tuple[Sequence[FiscalYearCompany], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [FiscalYearCompany.business_id == business_id]

        if parent_id is not None:

            conditions.append(FiscalYearCompany.parent_id == parent_id)

        total = int(

            db.scalar(

                select(func.count()).select_from(FiscalYearCompany).where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(FiscalYearCompany)

            .where(*conditions)

            .order_by(FiscalYearCompany.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

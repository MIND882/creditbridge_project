"""Data access for FinancialReportTemplate. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.financial_report_template_domain.models.financial_report_template import FinancialReportTemplate

from app.core.pagination import normalise_paging



__all__ = ["FinancialReportTemplateRepository"]





class FinancialReportTemplateRepository:

    model = FinancialReportTemplate



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(FinancialReportTemplate.rows)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[FinancialReportTemplate]:

        return db.scalar(

            select(FinancialReportTemplate).where(

                FinancialReportTemplate.business_id == business_id, FinancialReportTemplate.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[FinancialReportTemplate]:

        return db.scalar(

            select(FinancialReportTemplate).where(

                FinancialReportTemplate.business_id == business_id, FinancialReportTemplate.name == name

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

    ) -> tuple[Sequence[FinancialReportTemplate], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [FinancialReportTemplate.business_id == business_id]

        if search:

            conditions.append(FinancialReportTemplate.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(FinancialReportTemplate).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(FinancialReportTemplate)

            .where(*conditions)

            .order_by(FinancialReportTemplate.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: FinancialReportTemplate) -> FinancialReportTemplate:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: FinancialReportTemplate) -> None:

        db.delete(row)

        db.flush()

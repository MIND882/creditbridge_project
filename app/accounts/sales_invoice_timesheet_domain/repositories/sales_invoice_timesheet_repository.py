"""Data access for SalesInvoiceTimesheet. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.sales_invoice_timesheet_domain.models.sales_invoice_timesheet import SalesInvoiceTimesheet

from app.core.pagination import normalise_paging



__all__ = ["SalesInvoiceTimesheetRepository"]





class SalesInvoiceTimesheetRepository:

    model = SalesInvoiceTimesheet





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesInvoiceTimesheet]:

        return db.scalar(

            select(SalesInvoiceTimesheet).where(

                SalesInvoiceTimesheet.business_id == business_id, SalesInvoiceTimesheet.id == row_id

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

    ) -> tuple[Sequence[SalesInvoiceTimesheet], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesInvoiceTimesheet.business_id == business_id]

        if parent_id is not None:

            conditions.append(SalesInvoiceTimesheet.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SalesInvoiceTimesheet).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesInvoiceTimesheet)

            .where(*conditions)

            .order_by(SalesInvoiceTimesheet.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



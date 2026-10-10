"""Business logic for FinancialReportRow.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.financial_report_row_domain.models.financial_report_row import FinancialReportRow

from app.accounts.financial_report_row_domain.repositories.financial_report_row_repository import (

    FinancialReportRowRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["FinancialReportRowService"]





class FinancialReportRowService:

    def __init__(self, repository: Optional[FinancialReportRowRepository] = None) -> None:

        self.repository = repository or FinancialReportRowRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> FinancialReportRow:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Financial Report Row", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[FinancialReportRow]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[FinancialReportRow].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

"""Business logic for FiscalYearCompany.



A Frappe child table: rows are written through the parent (FiscalYear), so this

service only reads. There is no upstream controller logic to port.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.fiscal_year_company_domain.models.fiscal_year_company import FiscalYearCompany

from app.accounts.fiscal_year_company_domain.repositories.fiscal_year_company_repository import (

    FiscalYearCompanyRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["FiscalYearCompanyService"]





class FiscalYearCompanyService:

    def __init__(self, repository: Optional[FiscalYearCompanyRepository] = None) -> None:

        self.repository = repository or FiscalYearCompanyRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> FiscalYearCompany:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Fiscal Year Company", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[FiscalYearCompany]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[FiscalYearCompany].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

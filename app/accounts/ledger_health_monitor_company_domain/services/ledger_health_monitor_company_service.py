"""Business logic for LedgerHealthMonitorCompany.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.ledger_health_monitor_company_domain.models.ledger_health_monitor_company import LedgerHealthMonitorCompany

from app.accounts.ledger_health_monitor_company_domain.repositories.ledger_health_monitor_company_repository import (

    LedgerHealthMonitorCompanyRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["LedgerHealthMonitorCompanyService"]





class LedgerHealthMonitorCompanyService:

    def __init__(self, repository: Optional[LedgerHealthMonitorCompanyRepository] = None) -> None:

        self.repository = repository or LedgerHealthMonitorCompanyRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LedgerHealthMonitorCompany:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Ledger Health Monitor Company", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LedgerHealthMonitorCompany]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LedgerHealthMonitorCompany].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

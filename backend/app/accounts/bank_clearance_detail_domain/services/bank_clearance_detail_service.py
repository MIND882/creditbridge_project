"""Read-only service for BankClearanceDetail; writes go through BankClearance."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_clearance_detail_domain.models.bank_clearance_detail import BankClearanceDetail

from app.accounts.bank_clearance_detail_domain.repositories.bank_clearance_detail_repository import BankClearanceDetailRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankClearanceDetailService"]





class BankClearanceDetailService:

    def __init__(self, repository: Optional[BankClearanceDetailRepository] = None) -> None:

        self.repository = repository or BankClearanceDetailRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> BankClearanceDetail:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BankClearanceDetail", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[BankClearanceDetail]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankClearanceDetail].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

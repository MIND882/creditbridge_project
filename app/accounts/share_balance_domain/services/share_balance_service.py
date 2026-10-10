"""Business logic for ShareBalance.



A Frappe child table: rows are written through the parent (Shareholder), so this

service only reads. There is no upstream controller logic to port.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.share_balance_domain.models.share_balance import ShareBalance

from app.accounts.share_balance_domain.repositories.share_balance_repository import (

    ShareBalanceRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ShareBalanceService"]





class ShareBalanceService:

    def __init__(self, repository: Optional[ShareBalanceRepository] = None) -> None:

        self.repository = repository or ShareBalanceRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShareBalance:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Share Balance", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ShareBalance]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ShareBalance].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

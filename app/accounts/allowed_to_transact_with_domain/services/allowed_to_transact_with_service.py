"""Business logic for AllowedToTransactWith.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.allowed_to_transact_with_domain.models.allowed_to_transact_with import AllowedToTransactWith

from app.accounts.allowed_to_transact_with_domain.repositories.allowed_to_transact_with_repository import (

    AllowedToTransactWithRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["AllowedToTransactWithService"]





class AllowedToTransactWithService:

    def __init__(self, repository: Optional[AllowedToTransactWithRepository] = None) -> None:

        self.repository = repository or AllowedToTransactWithRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> AllowedToTransactWith:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Allowed To Transact With", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[AllowedToTransactWith]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[AllowedToTransactWith].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

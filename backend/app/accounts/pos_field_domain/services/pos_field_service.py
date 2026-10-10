"""Business logic for POSField.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.pos_field_domain.models.pos_field import POSField

from app.accounts.pos_field_domain.repositories.pos_field_repository import (

    POSFieldRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSFieldService"]





class POSFieldService:

    def __init__(self, repository: Optional[POSFieldRepository] = None) -> None:

        self.repository = repository or POSFieldRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSField:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Field", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSField]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSField].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

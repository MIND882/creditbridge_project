"""Business logic for RepostAllowedTypes.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.repost_allowed_types_domain.models.repost_allowed_types import RepostAllowedTypes

from app.accounts.repost_allowed_types_domain.repositories.repost_allowed_types_repository import (

    RepostAllowedTypesRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["RepostAllowedTypesService"]





class RepostAllowedTypesService:

    def __init__(self, repository: Optional[RepostAllowedTypesRepository] = None) -> None:

        self.repository = repository or RepostAllowedTypesRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostAllowedTypes:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Repost Allowed Types", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[RepostAllowedTypes]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[RepostAllowedTypes].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

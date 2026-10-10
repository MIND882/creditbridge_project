"""Business logic for POSItemGroup.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.pos_item_group_domain.models.pos_item_group import POSItemGroup

from app.accounts.pos_item_group_domain.repositories.pos_item_group_repository import (

    POSItemGroupRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSItemGroupService"]





class POSItemGroupService:

    def __init__(self, repository: Optional[POSItemGroupRepository] = None) -> None:

        self.repository = repository or POSItemGroupRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSItemGroup:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Item Group", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSItemGroup]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSItemGroup].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

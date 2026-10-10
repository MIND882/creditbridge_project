"""Business logic for POSCustomerGroup.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.pos_customer_group_domain.models.pos_customer_group import POSCustomerGroup

from app.accounts.pos_customer_group_domain.repositories.pos_customer_group_repository import (

    POSCustomerGroupRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSCustomerGroupService"]





class POSCustomerGroupService:

    def __init__(self, repository: Optional[POSCustomerGroupRepository] = None) -> None:

        self.repository = repository or POSCustomerGroupRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSCustomerGroup:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Customer Group", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSCustomerGroup]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSCustomerGroup].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

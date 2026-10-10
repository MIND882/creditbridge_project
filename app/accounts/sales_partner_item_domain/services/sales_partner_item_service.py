"""Business logic for SalesPartnerItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.sales_partner_item_domain.models.sales_partner_item import SalesPartnerItem

from app.accounts.sales_partner_item_domain.repositories.sales_partner_item_repository import (

    SalesPartnerItemRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SalesPartnerItemService"]





class SalesPartnerItemService:

    def __init__(self, repository: Optional[SalesPartnerItemRepository] = None) -> None:

        self.repository = repository or SalesPartnerItemRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesPartnerItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sales Partner Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesPartnerItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesPartnerItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

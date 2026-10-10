"""Business logic for QuotationItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.selling.quotation_item_domain.models.quotation_item import QuotationItem

from app.selling.quotation_item_domain.repositories.quotation_item_repository import (

    QuotationItemRepository,

)

from app.selling.quotation_item_domain.schemas.quotation_item import (

    QuotationItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["QuotationItemService"]





class QuotationItemService:

    def __init__(self, repository: Optional[QuotationItemRepository] = None) -> None:

        self.repository = repository or QuotationItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> QuotationItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Quotation Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[QuotationItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[QuotationItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

"""Business logic for StockEntryDetail.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.stock_entry_detail_domain.models.stock_entry_detail import StockEntryDetail

from app.stock.stock_entry_detail_domain.repositories.stock_entry_detail_repository import (

    StockEntryDetailRepository,

)

from app.stock.stock_entry_detail_domain.schemas.stock_entry_detail import (

    StockEntryDetailCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["StockEntryDetailService"]





class StockEntryDetailService:

    def __init__(self, repository: Optional[StockEntryDetailRepository] = None) -> None:

        self.repository = repository or StockEntryDetailRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockEntryDetail:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Stock Entry Detail", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[StockEntryDetail]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[StockEntryDetail].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

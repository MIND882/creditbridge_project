"""Read-only service for ItemWiseTaxDetail; writes go through the parent doctype."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.item_wise_tax_detail_domain.models.item_wise_tax_detail import ItemWiseTaxDetail

from app.accounts.item_wise_tax_detail_domain.repositories.item_wise_tax_detail_repository import ItemWiseTaxDetailRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemWiseTaxDetailService"]





class ItemWiseTaxDetailService:

    def __init__(self, repository: Optional[ItemWiseTaxDetailRepository] = None) -> None:

        self.repository = repository or ItemWiseTaxDetailRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> ItemWiseTaxDetail:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("ItemWiseTaxDetail", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[ItemWiseTaxDetail]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemWiseTaxDetail].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

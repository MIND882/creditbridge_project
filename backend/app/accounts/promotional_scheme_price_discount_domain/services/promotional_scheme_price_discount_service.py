"""Business logic for PromotionalSchemePriceDiscount.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.promotional_scheme_price_discount_domain.models.promotional_scheme_price_discount import PromotionalSchemePriceDiscount

from app.accounts.promotional_scheme_price_discount_domain.repositories.promotional_scheme_price_discount_repository import (

    PromotionalSchemePriceDiscountRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PromotionalSchemePriceDiscountService"]





class PromotionalSchemePriceDiscountService:

    def __init__(self, repository: Optional[PromotionalSchemePriceDiscountRepository] = None) -> None:

        self.repository = repository or PromotionalSchemePriceDiscountRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PromotionalSchemePriceDiscount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Promotional Scheme Price Discount", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PromotionalSchemePriceDiscount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PromotionalSchemePriceDiscount].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

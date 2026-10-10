"""Business logic for PromotionalSchemeProductDiscount.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.promotional_scheme_product_discount_domain.models.promotional_scheme_product_discount import PromotionalSchemeProductDiscount

from app.accounts.promotional_scheme_product_discount_domain.repositories.promotional_scheme_product_discount_repository import (

    PromotionalSchemeProductDiscountRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PromotionalSchemeProductDiscountService"]





class PromotionalSchemeProductDiscountService:

    def __init__(self, repository: Optional[PromotionalSchemeProductDiscountRepository] = None) -> None:

        self.repository = repository or PromotionalSchemeProductDiscountRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PromotionalSchemeProductDiscount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Promotional Scheme Product Discount", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PromotionalSchemeProductDiscount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PromotionalSchemeProductDiscount].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

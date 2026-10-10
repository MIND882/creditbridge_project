"""Business logic for VariantField.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.variant_field_domain.models.variant_field import VariantField

from app.stock.variant_field_domain.repositories.variant_field_repository import (

    VariantFieldRepository,

)

from app.stock.variant_field_domain.schemas.variant_field import (

    VariantFieldCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["VariantFieldService"]





class VariantFieldService:

    def __init__(self, repository: Optional[VariantFieldRepository] = None) -> None:

        self.repository = repository or VariantFieldRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> VariantField:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Variant Field", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[VariantField]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[VariantField].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

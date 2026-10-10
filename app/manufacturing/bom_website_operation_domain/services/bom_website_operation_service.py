"""Business logic for BomWebsiteOperation.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.bom_website_operation_domain.models.bom_website_operation import BomWebsiteOperation

from app.manufacturing.bom_website_operation_domain.repositories.bom_website_operation_repository import (

    BomWebsiteOperationRepository,

)

from app.manufacturing.bom_website_operation_domain.schemas.bom_website_operation import (

    BomWebsiteOperationCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BomWebsiteOperationService"]





class BomWebsiteOperationService:

    def __init__(self, repository: Optional[BomWebsiteOperationRepository] = None) -> None:

        self.repository = repository or BomWebsiteOperationRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomWebsiteOperation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BOM Website Operation", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BomWebsiteOperation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BomWebsiteOperation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

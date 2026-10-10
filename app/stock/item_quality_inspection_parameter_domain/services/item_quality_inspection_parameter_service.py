"""Business logic for ItemQualityInspectionParameter.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.item_quality_inspection_parameter_domain.models.item_quality_inspection_parameter import ItemQualityInspectionParameter

from app.stock.item_quality_inspection_parameter_domain.repositories.item_quality_inspection_parameter_repository import (

    ItemQualityInspectionParameterRepository,

)

from app.stock.item_quality_inspection_parameter_domain.schemas.item_quality_inspection_parameter import (

    ItemQualityInspectionParameterCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemQualityInspectionParameterService"]





class ItemQualityInspectionParameterService:

    def __init__(self, repository: Optional[ItemQualityInspectionParameterRepository] = None) -> None:

        self.repository = repository or ItemQualityInspectionParameterRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemQualityInspectionParameter:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Quality Inspection Parameter", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemQualityInspectionParameter]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemQualityInspectionParameter].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

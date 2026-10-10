"""Business logic for QualityInspectionReading.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.quality_inspection_reading_domain.models.quality_inspection_reading import QualityInspectionReading

from app.stock.quality_inspection_reading_domain.repositories.quality_inspection_reading_repository import (

    QualityInspectionReadingRepository,

)

from app.stock.quality_inspection_reading_domain.schemas.quality_inspection_reading import (

    QualityInspectionReadingCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["QualityInspectionReadingService"]





class QualityInspectionReadingService:

    def __init__(self, repository: Optional[QualityInspectionReadingRepository] = None) -> None:

        self.repository = repository or QualityInspectionReadingRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> QualityInspectionReading:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Quality Inspection Reading", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[QualityInspectionReading]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[QualityInspectionReading].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

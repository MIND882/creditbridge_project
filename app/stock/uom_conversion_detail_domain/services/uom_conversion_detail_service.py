"""Business logic for UomConversionDetail.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.uom_conversion_detail_domain.models.uom_conversion_detail import UomConversionDetail

from app.stock.uom_conversion_detail_domain.repositories.uom_conversion_detail_repository import (

    UomConversionDetailRepository,

)

from app.stock.uom_conversion_detail_domain.schemas.uom_conversion_detail import (

    UomConversionDetailCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["UomConversionDetailService"]





class UomConversionDetailService:

    def __init__(self, repository: Optional[UomConversionDetailRepository] = None) -> None:

        self.repository = repository or UomConversionDetailRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> UomConversionDetail:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("UOM Conversion Detail", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[UomConversionDetail]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[UomConversionDetail].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

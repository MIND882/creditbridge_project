"""Business logic for DeliveryStop.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.delivery_stop_domain.models.delivery_stop import DeliveryStop

from app.stock.delivery_stop_domain.repositories.delivery_stop_repository import (

    DeliveryStopRepository,

)

from app.stock.delivery_stop_domain.schemas.delivery_stop import (

    DeliveryStopCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["DeliveryStopService"]





class DeliveryStopService:

    def __init__(self, repository: Optional[DeliveryStopRepository] = None) -> None:

        self.repository = repository or DeliveryStopRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> DeliveryStop:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Delivery Stop", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[DeliveryStop]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[DeliveryStop].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

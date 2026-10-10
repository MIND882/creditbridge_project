"""Business logic for ShipmentParcel.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.shipment_parcel_domain.models.shipment_parcel import ShipmentParcel

from app.stock.shipment_parcel_domain.repositories.shipment_parcel_repository import (

    ShipmentParcelRepository,

)

from app.stock.shipment_parcel_domain.schemas.shipment_parcel import (

    ShipmentParcelCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ShipmentParcelService"]





class ShipmentParcelService:

    def __init__(self, repository: Optional[ShipmentParcelRepository] = None) -> None:

        self.repository = repository or ShipmentParcelRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShipmentParcel:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Shipment Parcel", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ShipmentParcel]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ShipmentParcel].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

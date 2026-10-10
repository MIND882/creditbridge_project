"""Business logic for LandedCostPurchaseReceipt.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.landed_cost_purchase_receipt_domain.models.landed_cost_purchase_receipt import LandedCostPurchaseReceipt

from app.stock.landed_cost_purchase_receipt_domain.repositories.landed_cost_purchase_receipt_repository import (

    LandedCostPurchaseReceiptRepository,

)

from app.stock.landed_cost_purchase_receipt_domain.schemas.landed_cost_purchase_receipt import (

    LandedCostPurchaseReceiptCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["LandedCostPurchaseReceiptService"]





class LandedCostPurchaseReceiptService:

    def __init__(self, repository: Optional[LandedCostPurchaseReceiptRepository] = None) -> None:

        self.repository = repository or LandedCostPurchaseReceiptRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LandedCostPurchaseReceipt:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Landed Cost Purchase Receipt", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LandedCostPurchaseReceipt]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LandedCostPurchaseReceipt].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

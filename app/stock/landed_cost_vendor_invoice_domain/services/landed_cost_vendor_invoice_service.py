"""Business logic for LandedCostVendorInvoice.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.landed_cost_vendor_invoice_domain.models.landed_cost_vendor_invoice import LandedCostVendorInvoice

from app.stock.landed_cost_vendor_invoice_domain.repositories.landed_cost_vendor_invoice_repository import (

    LandedCostVendorInvoiceRepository,

)

from app.stock.landed_cost_vendor_invoice_domain.schemas.landed_cost_vendor_invoice import (

    LandedCostVendorInvoiceCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["LandedCostVendorInvoiceService"]





class LandedCostVendorInvoiceService:

    def __init__(self, repository: Optional[LandedCostVendorInvoiceRepository] = None) -> None:

        self.repository = repository or LandedCostVendorInvoiceRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LandedCostVendorInvoice:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Landed Cost Vendor Invoice", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LandedCostVendorInvoice]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LandedCostVendorInvoice].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

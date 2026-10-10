"""Business logic for RequestForQuotationSupplier.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.buying.request_for_quotation_supplier_domain.models.request_for_quotation_supplier import RequestForQuotationSupplier

from app.buying.request_for_quotation_supplier_domain.repositories.request_for_quotation_supplier_repository import (

    RequestForQuotationSupplierRepository,

)

from app.buying.request_for_quotation_supplier_domain.schemas.request_for_quotation_supplier import (

    RequestForQuotationSupplierCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["RequestForQuotationSupplierService"]





class RequestForQuotationSupplierService:

    def __init__(self, repository: Optional[RequestForQuotationSupplierRepository] = None) -> None:

        self.repository = repository or RequestForQuotationSupplierRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RequestForQuotationSupplier:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Request for Quotation Supplier", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[RequestForQuotationSupplier]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[RequestForQuotationSupplier].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

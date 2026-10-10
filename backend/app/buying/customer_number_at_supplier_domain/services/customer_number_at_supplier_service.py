"""Business logic for CustomerNumberAtSupplier.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.buying.customer_number_at_supplier_domain.models.customer_number_at_supplier import CustomerNumberAtSupplier

from app.buying.customer_number_at_supplier_domain.repositories.customer_number_at_supplier_repository import (

    CustomerNumberAtSupplierRepository,

)

from app.buying.customer_number_at_supplier_domain.schemas.customer_number_at_supplier import (

    CustomerNumberAtSupplierCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["CustomerNumberAtSupplierService"]





class CustomerNumberAtSupplierService:

    def __init__(self, repository: Optional[CustomerNumberAtSupplierRepository] = None) -> None:

        self.repository = repository or CustomerNumberAtSupplierRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> CustomerNumberAtSupplier:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Customer Number At Supplier", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[CustomerNumberAtSupplier]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[CustomerNumberAtSupplier].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

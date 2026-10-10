"""Business logic for SupplierNumberAtCustomer.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.selling.supplier_number_at_customer_domain.models.supplier_number_at_customer import SupplierNumberAtCustomer

from app.selling.supplier_number_at_customer_domain.repositories.supplier_number_at_customer_repository import (

    SupplierNumberAtCustomerRepository,

)

from app.selling.supplier_number_at_customer_domain.schemas.supplier_number_at_customer import (

    SupplierNumberAtCustomerCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierNumberAtCustomerService"]





class SupplierNumberAtCustomerService:

    def __init__(self, repository: Optional[SupplierNumberAtCustomerRepository] = None) -> None:

        self.repository = repository or SupplierNumberAtCustomerRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierNumberAtCustomer:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Number At Customer", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierNumberAtCustomer]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierNumberAtCustomer].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

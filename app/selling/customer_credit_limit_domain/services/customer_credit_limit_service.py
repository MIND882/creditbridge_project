"""Business logic for CustomerCreditLimit.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.selling.customer_credit_limit_domain.models.customer_credit_limit import CustomerCreditLimit

from app.selling.customer_credit_limit_domain.repositories.customer_credit_limit_repository import (

    CustomerCreditLimitRepository,

)

from app.selling.customer_credit_limit_domain.schemas.customer_credit_limit import (

    CustomerCreditLimitCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["CustomerCreditLimitService"]





class CustomerCreditLimitService:

    def __init__(self, repository: Optional[CustomerCreditLimitRepository] = None) -> None:

        self.repository = repository or CustomerCreditLimitRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> CustomerCreditLimit:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Customer Credit Limit", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[CustomerCreditLimit]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[CustomerCreditLimit].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

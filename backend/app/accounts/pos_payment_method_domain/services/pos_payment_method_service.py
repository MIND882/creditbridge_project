"""Business logic for POSPaymentMethod.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.pos_payment_method_domain.models.pos_payment_method import POSPaymentMethod

from app.accounts.pos_payment_method_domain.repositories.pos_payment_method_repository import (

    POSPaymentMethodRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSPaymentMethodService"]





class POSPaymentMethodService:

    def __init__(self, repository: Optional[POSPaymentMethodRepository] = None) -> None:

        self.repository = repository or POSPaymentMethodRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSPaymentMethod:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Payment Method", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSPaymentMethod]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSPaymentMethod].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

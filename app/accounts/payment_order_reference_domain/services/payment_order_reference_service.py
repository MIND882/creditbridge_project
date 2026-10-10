"""Business logic for PaymentOrderReference.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.payment_order_reference_domain.models.payment_order_reference import PaymentOrderReference

from app.accounts.payment_order_reference_domain.repositories.payment_order_reference_repository import (

    PaymentOrderReferenceRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentOrderReferenceService"]





class PaymentOrderReferenceService:

    def __init__(self, repository: Optional[PaymentOrderReferenceRepository] = None) -> None:

        self.repository = repository or PaymentOrderReferenceRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentOrderReference:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Payment Order Reference", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentOrderReference]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentOrderReference].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

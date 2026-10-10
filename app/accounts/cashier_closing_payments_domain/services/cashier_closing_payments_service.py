"""Business logic for CashierClosingPayments.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.cashier_closing_payments_domain.models.cashier_closing_payments import CashierClosingPayments

from app.accounts.cashier_closing_payments_domain.repositories.cashier_closing_payments_repository import (

    CashierClosingPaymentsRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["CashierClosingPaymentsService"]





class CashierClosingPaymentsService:

    def __init__(self, repository: Optional[CashierClosingPaymentsRepository] = None) -> None:

        self.repository = repository or CashierClosingPaymentsRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> CashierClosingPayments:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Cashier Closing Payments", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[CashierClosingPayments]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[CashierClosingPayments].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

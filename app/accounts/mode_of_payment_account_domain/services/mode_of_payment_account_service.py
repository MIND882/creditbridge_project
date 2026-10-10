"""Business logic for ModeOfPaymentAccount.



A Frappe child table: rows are written through the parent (ModeOfPayment), so this

service only reads. There is no upstream controller logic to port.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.mode_of_payment_account_domain.models.mode_of_payment_account import ModeOfPaymentAccount

from app.accounts.mode_of_payment_account_domain.repositories.mode_of_payment_account_repository import (

    ModeOfPaymentAccountRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ModeOfPaymentAccountService"]





class ModeOfPaymentAccountService:

    def __init__(self, repository: Optional[ModeOfPaymentAccountRepository] = None) -> None:

        self.repository = repository or ModeOfPaymentAccountRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ModeOfPaymentAccount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Mode of Payment Account", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ModeOfPaymentAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ModeOfPaymentAccount].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

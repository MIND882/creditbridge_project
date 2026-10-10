"""Business logic for PeggedCurrencyDetails.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.pegged_currency_details_domain.models.pegged_currency_details import PeggedCurrencyDetails

from app.accounts.pegged_currency_details_domain.repositories.pegged_currency_details_repository import (

    PeggedCurrencyDetailsRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PeggedCurrencyDetailsService"]





class PeggedCurrencyDetailsService:

    def __init__(self, repository: Optional[PeggedCurrencyDetailsRepository] = None) -> None:

        self.repository = repository or PeggedCurrencyDetailsRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PeggedCurrencyDetails:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Pegged Currency Details", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PeggedCurrencyDetails]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PeggedCurrencyDetails].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

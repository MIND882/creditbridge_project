"""Business logic for CurrencyExchangeSettingsDetails.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.currency_exchange_settings_details_domain.models.currency_exchange_settings_details import CurrencyExchangeSettingsDetails

from app.accounts.currency_exchange_settings_details_domain.repositories.currency_exchange_settings_details_repository import (

    CurrencyExchangeSettingsDetailsRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["CurrencyExchangeSettingsDetailsService"]





class CurrencyExchangeSettingsDetailsService:

    def __init__(self, repository: Optional[CurrencyExchangeSettingsDetailsRepository] = None) -> None:

        self.repository = repository or CurrencyExchangeSettingsDetailsRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> CurrencyExchangeSettingsDetails:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Currency Exchange Settings Details", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[CurrencyExchangeSettingsDetails]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[CurrencyExchangeSettingsDetails].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

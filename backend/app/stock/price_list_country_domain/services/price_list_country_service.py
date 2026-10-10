"""Business logic for PriceListCountry.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.price_list_country_domain.models.price_list_country import PriceListCountry

from app.stock.price_list_country_domain.repositories.price_list_country_repository import (

    PriceListCountryRepository,

)

from app.stock.price_list_country_domain.schemas.price_list_country import (

    PriceListCountryCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PriceListCountryService"]





class PriceListCountryService:

    def __init__(self, repository: Optional[PriceListCountryRepository] = None) -> None:

        self.repository = repository or PriceListCountryRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PriceListCountry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Price List Country", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PriceListCountry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PriceListCountry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

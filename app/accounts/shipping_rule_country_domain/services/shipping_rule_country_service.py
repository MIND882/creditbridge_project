"""Business logic for ShippingRuleCountry.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.shipping_rule_country_domain.models.shipping_rule_country import ShippingRuleCountry

from app.accounts.shipping_rule_country_domain.repositories.shipping_rule_country_repository import (

    ShippingRuleCountryRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ShippingRuleCountryService"]





class ShippingRuleCountryService:

    def __init__(self, repository: Optional[ShippingRuleCountryRepository] = None) -> None:

        self.repository = repository or ShippingRuleCountryRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShippingRuleCountry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Shipping Rule Country", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ShippingRuleCountry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ShippingRuleCountry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

"""Business logic for LandedCostTaxesAndCharges.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.landed_cost_taxes_and_charges_domain.models.landed_cost_taxes_and_charges import LandedCostTaxesAndCharges

from app.stock.landed_cost_taxes_and_charges_domain.repositories.landed_cost_taxes_and_charges_repository import (

    LandedCostTaxesAndChargesRepository,

)

from app.stock.landed_cost_taxes_and_charges_domain.schemas.landed_cost_taxes_and_charges import (

    LandedCostTaxesAndChargesCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["LandedCostTaxesAndChargesService"]





class LandedCostTaxesAndChargesService:

    def __init__(self, repository: Optional[LandedCostTaxesAndChargesRepository] = None) -> None:

        self.repository = repository or LandedCostTaxesAndChargesRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LandedCostTaxesAndCharges:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Landed Cost Taxes and Charges", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LandedCostTaxesAndCharges]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LandedCostTaxesAndCharges].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

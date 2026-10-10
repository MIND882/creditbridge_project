"""Read-only service for TaxWithholdingRate; writes go through the parent doctype."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.tax_withholding_rate_domain.models.tax_withholding_rate import TaxWithholdingRate

from app.accounts.tax_withholding_rate_domain.repositories.tax_withholding_rate_repository import TaxWithholdingRateRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["TaxWithholdingRateService"]





class TaxWithholdingRateService:

    def __init__(self, repository: Optional[TaxWithholdingRateRepository] = None) -> None:

        self.repository = repository or TaxWithholdingRateRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> TaxWithholdingRate:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("TaxWithholdingRate", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[TaxWithholdingRate]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[TaxWithholdingRate].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

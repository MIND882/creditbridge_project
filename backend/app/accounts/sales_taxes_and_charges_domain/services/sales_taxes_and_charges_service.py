"""Read-only service for SalesTaxesAndCharges; writes go through the parent doctype."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.sales_taxes_and_charges_domain.models.sales_taxes_and_charges import SalesTaxesAndCharges

from app.accounts.sales_taxes_and_charges_domain.repositories.sales_taxes_and_charges_repository import SalesTaxesAndChargesRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SalesTaxesAndChargesService"]





class SalesTaxesAndChargesService:

    def __init__(self, repository: Optional[SalesTaxesAndChargesRepository] = None) -> None:

        self.repository = repository or SalesTaxesAndChargesRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> SalesTaxesAndCharges:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("SalesTaxesAndCharges", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[SalesTaxesAndCharges]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesTaxesAndCharges].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

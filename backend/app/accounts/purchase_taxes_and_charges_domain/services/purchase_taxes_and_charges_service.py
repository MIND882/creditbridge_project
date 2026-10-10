"""Read-only service for PurchaseTaxesAndCharges; writes go through the parent doctype."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.purchase_taxes_and_charges_domain.models.purchase_taxes_and_charges import PurchaseTaxesAndCharges

from app.accounts.purchase_taxes_and_charges_domain.repositories.purchase_taxes_and_charges_repository import PurchaseTaxesAndChargesRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PurchaseTaxesAndChargesService"]





class PurchaseTaxesAndChargesService:

    def __init__(self, repository: Optional[PurchaseTaxesAndChargesRepository] = None) -> None:

        self.repository = repository or PurchaseTaxesAndChargesRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> PurchaseTaxesAndCharges:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("PurchaseTaxesAndCharges", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[PurchaseTaxesAndCharges]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PurchaseTaxesAndCharges].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

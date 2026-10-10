"""Read-only service for AdvanceTaxesAndCharges; writes go through the parent doctype."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.advance_taxes_and_charges_domain.models.advance_taxes_and_charges import AdvanceTaxesAndCharges

from app.accounts.advance_taxes_and_charges_domain.repositories.advance_taxes_and_charges_repository import AdvanceTaxesAndChargesRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["AdvanceTaxesAndChargesService"]





class AdvanceTaxesAndChargesService:

    def __init__(self, repository: Optional[AdvanceTaxesAndChargesRepository] = None) -> None:

        self.repository = repository or AdvanceTaxesAndChargesRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> AdvanceTaxesAndCharges:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("AdvanceTaxesAndCharges", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[AdvanceTaxesAndCharges]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[AdvanceTaxesAndCharges].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )

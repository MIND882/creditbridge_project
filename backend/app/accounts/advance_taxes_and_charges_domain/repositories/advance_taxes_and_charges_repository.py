"""Data access for AdvanceTaxesAndCharges. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.advance_taxes_and_charges_domain.models.advance_taxes_and_charges import AdvanceTaxesAndCharges

from app.core.pagination import normalise_paging



__all__ = ["AdvanceTaxesAndChargesRepository"]





class AdvanceTaxesAndChargesRepository:

    model = AdvanceTaxesAndCharges



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[AdvanceTaxesAndCharges]:

        return db.scalar(

            select(AdvanceTaxesAndCharges).where(

                AdvanceTaxesAndCharges.business_id == business_id, AdvanceTaxesAndCharges.id == row_id

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[AdvanceTaxesAndCharges], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [AdvanceTaxesAndCharges.business_id == business_id]

        if parent_id is not None:

            conditions.append(AdvanceTaxesAndCharges.parent_id == parent_id)

        total = int(

            db.scalar(select(func.count()).select_from(AdvanceTaxesAndCharges).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(AdvanceTaxesAndCharges)

            .where(*conditions)

            .order_by(AdvanceTaxesAndCharges.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

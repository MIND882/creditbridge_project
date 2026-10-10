"""Data access for LandedCostTaxesAndCharges. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.landed_cost_taxes_and_charges_domain.models.landed_cost_taxes_and_charges import LandedCostTaxesAndCharges

from app.core.pagination import normalise_paging



__all__ = ["LandedCostTaxesAndChargesRepository"]





class LandedCostTaxesAndChargesRepository:

    model = LandedCostTaxesAndCharges





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LandedCostTaxesAndCharges]:

        return db.scalar(

            select(LandedCostTaxesAndCharges).where(

                LandedCostTaxesAndCharges.business_id == business_id, LandedCostTaxesAndCharges.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[LandedCostTaxesAndCharges]:

        return db.scalar(

            select(LandedCostTaxesAndCharges).where(

                LandedCostTaxesAndCharges.business_id == business_id, LandedCostTaxesAndCharges.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[LandedCostTaxesAndCharges], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LandedCostTaxesAndCharges.business_id == business_id]

        if parent_id is not None:

            conditions.append(LandedCostTaxesAndCharges.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(LandedCostTaxesAndCharges).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LandedCostTaxesAndCharges)

            .where(*conditions)

            .order_by(LandedCostTaxesAndCharges.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

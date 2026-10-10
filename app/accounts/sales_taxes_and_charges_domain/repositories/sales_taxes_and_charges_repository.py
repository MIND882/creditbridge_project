"""Data access for SalesTaxesAndCharges. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.sales_taxes_and_charges_domain.models.sales_taxes_and_charges import SalesTaxesAndCharges

from app.core.pagination import normalise_paging



__all__ = ["SalesTaxesAndChargesRepository"]





class SalesTaxesAndChargesRepository:

    model = SalesTaxesAndCharges



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[SalesTaxesAndCharges]:

        return db.scalar(

            select(SalesTaxesAndCharges).where(

                SalesTaxesAndCharges.business_id == business_id, SalesTaxesAndCharges.id == row_id

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

    ) -> tuple[Sequence[SalesTaxesAndCharges], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesTaxesAndCharges.business_id == business_id]

        if parent_id is not None:

            conditions.append(SalesTaxesAndCharges.parent_id == parent_id)

        total = int(

            db.scalar(select(func.count()).select_from(SalesTaxesAndCharges).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(SalesTaxesAndCharges)

            .where(*conditions)

            .order_by(SalesTaxesAndCharges.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

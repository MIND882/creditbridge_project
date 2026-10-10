"""Data access for LandedCostVendorInvoice. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.landed_cost_vendor_invoice_domain.models.landed_cost_vendor_invoice import LandedCostVendorInvoice

from app.core.pagination import normalise_paging



__all__ = ["LandedCostVendorInvoiceRepository"]





class LandedCostVendorInvoiceRepository:

    model = LandedCostVendorInvoice





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LandedCostVendorInvoice]:

        return db.scalar(

            select(LandedCostVendorInvoice).where(

                LandedCostVendorInvoice.business_id == business_id, LandedCostVendorInvoice.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[LandedCostVendorInvoice]:

        return db.scalar(

            select(LandedCostVendorInvoice).where(

                LandedCostVendorInvoice.business_id == business_id, LandedCostVendorInvoice.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[LandedCostVendorInvoice], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LandedCostVendorInvoice.business_id == business_id]

        if parent_id is not None:

            conditions.append(LandedCostVendorInvoice.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(LandedCostVendorInvoice).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LandedCostVendorInvoice)

            .where(*conditions)

            .order_by(LandedCostVendorInvoice.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

"""Data access for SupplierQuotationItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_quotation_item_domain.models.supplier_quotation_item import SupplierQuotationItem

from app.core.pagination import normalise_paging



__all__ = ["SupplierQuotationItemRepository"]





class SupplierQuotationItemRepository:

    model = SupplierQuotationItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierQuotationItem]:

        return db.scalar(

            select(SupplierQuotationItem).where(

                SupplierQuotationItem.business_id == business_id, SupplierQuotationItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierQuotationItem]:

        return db.scalar(

            select(SupplierQuotationItem).where(

                SupplierQuotationItem.business_id == business_id, SupplierQuotationItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[SupplierQuotationItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierQuotationItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(SupplierQuotationItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SupplierQuotationItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierQuotationItem)

            .where(*conditions)

            .order_by(SupplierQuotationItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

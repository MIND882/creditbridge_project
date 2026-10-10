"""Data access for SupplierItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.supplier_item_domain.models.supplier_item import SupplierItem

from app.core.pagination import normalise_paging



__all__ = ["SupplierItemRepository"]





class SupplierItemRepository:

    model = SupplierItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierItem]:

        return db.scalar(

            select(SupplierItem).where(

                SupplierItem.business_id == business_id, SupplierItem.id == row_id

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

    ) -> tuple[Sequence[SupplierItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(SupplierItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SupplierItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierItem)

            .where(*conditions)

            .order_by(SupplierItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



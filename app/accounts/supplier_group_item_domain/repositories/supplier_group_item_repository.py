"""Data access for SupplierGroupItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.supplier_group_item_domain.models.supplier_group_item import SupplierGroupItem

from app.core.pagination import normalise_paging



__all__ = ["SupplierGroupItemRepository"]





class SupplierGroupItemRepository:

    model = SupplierGroupItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierGroupItem]:

        return db.scalar(

            select(SupplierGroupItem).where(

                SupplierGroupItem.business_id == business_id, SupplierGroupItem.id == row_id

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

    ) -> tuple[Sequence[SupplierGroupItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierGroupItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(SupplierGroupItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SupplierGroupItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierGroupItem)

            .where(*conditions)

            .order_by(SupplierGroupItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



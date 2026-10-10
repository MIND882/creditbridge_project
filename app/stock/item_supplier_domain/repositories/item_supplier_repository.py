"""Data access for ItemSupplier. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_supplier_domain.models.item_supplier import ItemSupplier

from app.core.pagination import normalise_paging



__all__ = ["ItemSupplierRepository"]





class ItemSupplierRepository:

    model = ItemSupplier





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemSupplier]:

        return db.scalar(

            select(ItemSupplier).where(

                ItemSupplier.business_id == business_id, ItemSupplier.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemSupplier]:

        return db.scalar(

            select(ItemSupplier).where(

                ItemSupplier.business_id == business_id, ItemSupplier.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ItemSupplier], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemSupplier.business_id == business_id]

        if parent_id is not None:

            conditions.append(ItemSupplier.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ItemSupplier).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemSupplier)

            .where(*conditions)

            .order_by(ItemSupplier.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

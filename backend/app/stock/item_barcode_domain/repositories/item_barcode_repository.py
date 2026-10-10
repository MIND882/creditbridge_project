"""Data access for ItemBarcode. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_barcode_domain.models.item_barcode import ItemBarcode

from app.core.pagination import normalise_paging



__all__ = ["ItemBarcodeRepository"]





class ItemBarcodeRepository:

    model = ItemBarcode





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemBarcode]:

        return db.scalar(

            select(ItemBarcode).where(

                ItemBarcode.business_id == business_id, ItemBarcode.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ItemBarcode], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemBarcode.business_id == business_id]

        if parent_id is not None:

            conditions.append(ItemBarcode.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ItemBarcode).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemBarcode)

            .where(*conditions)

            .order_by(ItemBarcode.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

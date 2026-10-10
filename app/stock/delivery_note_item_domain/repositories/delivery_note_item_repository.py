"""Data access for DeliveryNoteItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.delivery_note_item_domain.models.delivery_note_item import DeliveryNoteItem

from app.core.pagination import normalise_paging



__all__ = ["DeliveryNoteItemRepository"]





class DeliveryNoteItemRepository:

    model = DeliveryNoteItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[DeliveryNoteItem]:

        return db.scalar(

            select(DeliveryNoteItem).where(

                DeliveryNoteItem.business_id == business_id, DeliveryNoteItem.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[DeliveryNoteItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [DeliveryNoteItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(DeliveryNoteItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(DeliveryNoteItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(DeliveryNoteItem)

            .where(*conditions)

            .order_by(DeliveryNoteItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

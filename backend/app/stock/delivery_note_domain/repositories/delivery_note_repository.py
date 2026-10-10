"""Data access for DeliveryNote. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.delivery_note_domain.models.delivery_note import DeliveryNote

from app.core.pagination import normalise_paging



__all__ = ["DeliveryNoteRepository"]





class DeliveryNoteRepository:

    model = DeliveryNote





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[DeliveryNote]:

        return db.scalar(

            select(DeliveryNote).where(

                DeliveryNote.business_id == business_id, DeliveryNote.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[DeliveryNote]:

        return db.scalar(

            select(DeliveryNote).where(

                DeliveryNote.business_id == business_id, DeliveryNote.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[DeliveryNote], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [DeliveryNote.business_id == business_id]

        if not include_cancelled:

            conditions.append(DeliveryNote.docstatus != 2)

        if search:

            conditions.append(DeliveryNote.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(DeliveryNote).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(DeliveryNote)

            .where(*conditions)

            .order_by(DeliveryNote.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: DeliveryNote) -> DeliveryNote:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: DeliveryNote) -> None:

        db.delete(row)

        db.flush()

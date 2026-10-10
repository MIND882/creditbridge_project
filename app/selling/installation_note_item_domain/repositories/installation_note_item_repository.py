"""Data access for InstallationNoteItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.installation_note_item_domain.models.installation_note_item import InstallationNoteItem

from app.core.pagination import normalise_paging



__all__ = ["InstallationNoteItemRepository"]





class InstallationNoteItemRepository:

    model = InstallationNoteItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[InstallationNoteItem]:

        return db.scalar(

            select(InstallationNoteItem).where(

                InstallationNoteItem.business_id == business_id, InstallationNoteItem.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[InstallationNoteItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [InstallationNoteItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(InstallationNoteItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(InstallationNoteItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(InstallationNoteItem)

            .where(*conditions)

            .order_by(InstallationNoteItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

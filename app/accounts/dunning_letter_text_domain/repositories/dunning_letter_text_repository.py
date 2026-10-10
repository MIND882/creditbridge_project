"""Data access for DunningLetterText. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.dunning_letter_text_domain.models.dunning_letter_text import DunningLetterText

from app.core.pagination import normalise_paging



__all__ = ["DunningLetterTextRepository"]





class DunningLetterTextRepository:

    model = DunningLetterText



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[DunningLetterText]:

        return db.scalar(

            select(DunningLetterText).where(

                DunningLetterText.business_id == business_id, DunningLetterText.id == row_id

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

    ) -> tuple[Sequence[DunningLetterText], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [DunningLetterText.business_id == business_id]

        if parent_id is not None:

            conditions.append(DunningLetterText.parent_id == parent_id)

        total = int(

            db.scalar(select(func.count()).select_from(DunningLetterText).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(DunningLetterText)

            .where(*conditions)

            .order_by(DunningLetterText.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

"""Data access for PutawayRule. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.putaway_rule_domain.models.putaway_rule import PutawayRule

from app.core.pagination import normalise_paging



__all__ = ["PutawayRuleRepository"]





class PutawayRuleRepository:

    model = PutawayRule





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PutawayRule]:

        return db.scalar(

            select(PutawayRule).where(

                PutawayRule.business_id == business_id, PutawayRule.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PutawayRule]:

        return db.scalar(

            select(PutawayRule).where(

                PutawayRule.business_id == business_id, PutawayRule.name == name

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

    ) -> tuple[Sequence[PutawayRule], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PutawayRule.business_id == business_id]

        if search:

            conditions.append(PutawayRule.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PutawayRule).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PutawayRule)

            .where(*conditions)

            .order_by(PutawayRule.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: PutawayRule) -> PutawayRule:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PutawayRule) -> None:

        db.delete(row)

        db.flush()

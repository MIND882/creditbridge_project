"""Data access for RepostItemValuation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.repost_item_valuation_domain.models.repost_item_valuation import RepostItemValuation

from app.core.pagination import normalise_paging



__all__ = ["RepostItemValuationRepository"]





class RepostItemValuationRepository:

    model = RepostItemValuation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[RepostItemValuation]:

        return db.scalar(

            select(RepostItemValuation).where(

                RepostItemValuation.business_id == business_id, RepostItemValuation.id == row_id

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

    ) -> tuple[Sequence[RepostItemValuation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [RepostItemValuation.business_id == business_id]

        if not include_cancelled:

            conditions.append(RepostItemValuation.docstatus != 2)

        if search:

            conditions.append(RepostItemValuation.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(RepostItemValuation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(RepostItemValuation)

            .where(*conditions)

            .order_by(RepostItemValuation.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: RepostItemValuation) -> RepostItemValuation:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: RepostItemValuation) -> None:

        db.delete(row)

        db.flush()

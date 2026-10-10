"""Data access for ShareBalance. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.share_balance_domain.models.share_balance import ShareBalance

from app.core.pagination import normalise_paging



__all__ = ["ShareBalanceRepository"]





class ShareBalanceRepository:

    model = ShareBalance



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ShareBalance]:

        return db.scalar(

            select(ShareBalance).where(

                ShareBalance.business_id == business_id,

                ShareBalance.id == row_id,

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

    ) -> tuple[Sequence[ShareBalance], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ShareBalance.business_id == business_id]

        if parent_id is not None:

            conditions.append(ShareBalance.parent_id == parent_id)

        total = int(

            db.scalar(

                select(func.count()).select_from(ShareBalance).where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(ShareBalance)

            .where(*conditions)

            .order_by(ShareBalance.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

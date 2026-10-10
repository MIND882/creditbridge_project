"""Data access for RepostPaymentLedgerItems. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.repost_payment_ledger_items_domain.models.repost_payment_ledger_items import RepostPaymentLedgerItems

from app.core.pagination import normalise_paging



__all__ = ["RepostPaymentLedgerItemsRepository"]





class RepostPaymentLedgerItemsRepository:

    model = RepostPaymentLedgerItems





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[RepostPaymentLedgerItems]:

        return db.scalar(

            select(RepostPaymentLedgerItems).where(

                RepostPaymentLedgerItems.business_id == business_id, RepostPaymentLedgerItems.id == row_id

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

    ) -> tuple[Sequence[RepostPaymentLedgerItems], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [RepostPaymentLedgerItems.business_id == business_id]

        if parent_id is not None:

            conditions.append(RepostPaymentLedgerItems.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(RepostPaymentLedgerItems).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(RepostPaymentLedgerItems)

            .where(*conditions)

            .order_by(RepostPaymentLedgerItems.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



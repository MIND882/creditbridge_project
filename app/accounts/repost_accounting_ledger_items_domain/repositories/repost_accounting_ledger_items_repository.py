"""Data access for RepostAccountingLedgerItems. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.repost_accounting_ledger_items_domain.models.repost_accounting_ledger_items import RepostAccountingLedgerItems

from app.core.pagination import normalise_paging



__all__ = ["RepostAccountingLedgerItemsRepository"]





class RepostAccountingLedgerItemsRepository:

    model = RepostAccountingLedgerItems





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[RepostAccountingLedgerItems]:

        return db.scalar(

            select(RepostAccountingLedgerItems).where(

                RepostAccountingLedgerItems.business_id == business_id, RepostAccountingLedgerItems.id == row_id

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

    ) -> tuple[Sequence[RepostAccountingLedgerItems], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [RepostAccountingLedgerItems.business_id == business_id]

        if parent_id is not None:

            conditions.append(RepostAccountingLedgerItems.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(RepostAccountingLedgerItems).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(RepostAccountingLedgerItems)

            .where(*conditions)

            .order_by(RepostAccountingLedgerItems.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



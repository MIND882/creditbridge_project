"""Data access for LedgerMergeAccounts. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.ledger_merge_accounts_domain.models.ledger_merge_accounts import LedgerMergeAccounts

from app.core.pagination import normalise_paging



__all__ = ["LedgerMergeAccountsRepository"]





class LedgerMergeAccountsRepository:

    model = LedgerMergeAccounts





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LedgerMergeAccounts]:

        return db.scalar(

            select(LedgerMergeAccounts).where(

                LedgerMergeAccounts.business_id == business_id, LedgerMergeAccounts.id == row_id

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

    ) -> tuple[Sequence[LedgerMergeAccounts], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LedgerMergeAccounts.business_id == business_id]

        if parent_id is not None:

            conditions.append(LedgerMergeAccounts.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(LedgerMergeAccounts).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LedgerMergeAccounts)

            .where(*conditions)

            .order_by(LedgerMergeAccounts.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



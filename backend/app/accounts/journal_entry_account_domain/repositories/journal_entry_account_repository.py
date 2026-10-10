"""Data access for JournalEntryAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.journal_entry_account_domain.models.journal_entry_account import JournalEntryAccount

from app.core.pagination import normalise_paging



__all__ = ["JournalEntryAccountRepository"]





class JournalEntryAccountRepository:

    model = JournalEntryAccount



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[JournalEntryAccount]:

        return db.scalar(select(JournalEntryAccount).where(JournalEntryAccount.business_id == business_id, JournalEntryAccount.id == row_id))



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[JournalEntryAccount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [JournalEntryAccount.business_id == business_id]

        if parent_id is not None:

            conditions.append(JournalEntryAccount.parent_id == parent_id)

        total = int(db.scalar(select(func.count()).select_from(JournalEntryAccount).where(*conditions)) or 0)

        rows = db.scalars(

            select(JournalEntryAccount).where(*conditions).order_by(JournalEntryAccount.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total

"""Data access for JournalEntryTemplateAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.journal_entry_template_account_domain.models.journal_entry_template_account import JournalEntryTemplateAccount

from app.core.pagination import normalise_paging



__all__ = ["JournalEntryTemplateAccountRepository"]





class JournalEntryTemplateAccountRepository:

    model = JournalEntryTemplateAccount



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[JournalEntryTemplateAccount]:

        return db.scalar(

            select(JournalEntryTemplateAccount).where(

                JournalEntryTemplateAccount.business_id == business_id,

                JournalEntryTemplateAccount.id == row_id,

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

    ) -> tuple[Sequence[JournalEntryTemplateAccount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [JournalEntryTemplateAccount.business_id == business_id]

        if parent_id is not None:

            conditions.append(JournalEntryTemplateAccount.parent_id == parent_id)

        total = int(

            db.scalar(

                select(func.count()).select_from(JournalEntryTemplateAccount).where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(JournalEntryTemplateAccount)

            .where(*conditions)

            .order_by(JournalEntryTemplateAccount.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

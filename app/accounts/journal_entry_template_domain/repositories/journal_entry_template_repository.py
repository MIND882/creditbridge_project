"""Data access for JournalEntryTemplate. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.journal_entry_domain.models.journal_entry import JournalVoucherType

from app.accounts.journal_entry_template_domain.models.journal_entry_template import (

    JournalEntryTemplate,

)

from app.core.pagination import normalise_paging



__all__ = ["JournalEntryTemplateRepository"]





class JournalEntryTemplateRepository:

    model = JournalEntryTemplate



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks conftest

        # collection with "failed to locate a name".

        return [selectinload(JournalEntryTemplate.accounts)]



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[JournalEntryTemplate]:

        return db.scalar(

            select(JournalEntryTemplate)

            .where(

                JournalEntryTemplate.business_id == business_id,

                JournalEntryTemplate.id == row_id,

            )

            .options(*self._options())

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[JournalEntryTemplate]:

        return db.scalar(

            select(JournalEntryTemplate)

            .where(

                JournalEntryTemplate.business_id == business_id,

                JournalEntryTemplate.name == name,

            )

            .options(*self._options())

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        voucher_type: Optional[JournalVoucherType] = None,

        search: Optional[str] = None,

    ) -> tuple[Sequence[JournalEntryTemplate], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [JournalEntryTemplate.business_id == business_id]

        if voucher_type is not None:

            conditions.append(JournalEntryTemplate.voucher_type == voucher_type)

        if search:

            conditions.append(

                JournalEntryTemplate.name.ilike(f"%{search.strip()}%")

            )



        total = int(

            db.scalar(

                select(func.count())

                .select_from(JournalEntryTemplate)

                .where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(JournalEntryTemplate)

            .where(*conditions)

            .order_by(JournalEntryTemplate.name.asc())

            .offset(offset)

            .limit(limit)

            .options(*self._options())

        ).all()

        return rows, total



    def add(self, db: Session, row: JournalEntryTemplate) -> JournalEntryTemplate:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: JournalEntryTemplate) -> None:

        db.delete(row)

        db.flush()

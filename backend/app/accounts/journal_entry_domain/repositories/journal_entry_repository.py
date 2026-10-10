"""Data access for Journal Entry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.journal_entry_domain.models.journal_entry import JournalEntry

from app.core.pagination import normalise_paging



__all__ = ["JournalEntryRepository"]





class JournalEntryRepository:

    model = JournalEntry



    @staticmethod

    def _eager() -> tuple:

        """Loader options, built on demand -- a class attribute would force

        mapper configuration at import time and break conftest collection."""

        return (selectinload(JournalEntry.accounts),)



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID

    ) -> Optional[JournalEntry]:

        return db.scalar(

            select(JournalEntry)

            .options(*self._eager())

            .where(

                JournalEntry.business_id == business_id, JournalEntry.id == entry_id

            )

        )



    def get_by_name(self, db: Session, business_id: uuid.UUID, name: str) -> Optional[JournalEntry]:

        return db.scalar(

            select(JournalEntry).where(

                JournalEntry.business_id == business_id, JournalEntry.name == name

            )

        )



    def next_name(self, db: Session, business_id: uuid.UUID, on: date) -> str:

        """``ACC-JV-.YYYY.-#####``, counter scoped per tenant and year."""

        start, end = date(on.year, 1, 1), date(on.year, 12, 31)

        count = int(

            db.scalar(

                select(func.count())

                .select_from(JournalEntry)

                .where(

                    JournalEntry.business_id == business_id,

                    JournalEntry.created_at >= start,

                    JournalEntry.created_at <= end,

                )

            )

            or 0

        )

        return f"ACC-JV-{on.year}-{count + 1:05d}"



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        voucher_type: Optional[str] = None,

        from_date: Optional[date] = None,

        to_date: Optional[date] = None,

        search: Optional[str] = None,

        docstatus: Optional[int] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[JournalEntry], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [JournalEntry.business_id == business_id]

        if voucher_type:

            conditions.append(JournalEntry.voucher_type == voucher_type)

        if from_date is not None:

            conditions.append(JournalEntry.posting_date >= from_date)

        if to_date is not None:

            conditions.append(JournalEntry.posting_date <= to_date)

        if search:

            pattern = f"%{search}%"

            conditions.append(

                JournalEntry.title.ilike(pattern)

                | JournalEntry.name.ilike(pattern)

                | JournalEntry.remark.ilike(pattern)

                | JournalEntry.user_remark.ilike(pattern)

            )

        if docstatus is not None:

            conditions.append(JournalEntry.docstatus == docstatus)

        elif not include_cancelled:

            conditions.append(JournalEntry.docstatus != 2)



        total = int(

            db.scalar(select(func.count()).select_from(JournalEntry).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(JournalEntry)

            .options(*self._eager())

            .where(*conditions)

            .order_by(JournalEntry.posting_date.desc(), JournalEntry.name.desc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, entry: JournalEntry) -> JournalEntry:

        db.add(entry)

        db.flush()

        return entry



    def delete(self, db: Session, entry: JournalEntry) -> None:

        db.delete(entry)

        db.flush()

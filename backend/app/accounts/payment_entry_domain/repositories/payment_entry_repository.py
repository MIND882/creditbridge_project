"""Data access for Payment Entry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.payment_entry_domain.models.payment_entry import PaymentEntry

from app.core.pagination import normalise_paging



__all__ = ["PaymentEntryRepository"]





class PaymentEntryRepository:

    model = PaymentEntry



    @staticmethod

    def _eager() -> tuple:

        """Loader options, built on demand -- a class attribute would force

        mapper configuration at import time and break conftest collection."""

        return (

            selectinload(PaymentEntry.references),

            selectinload(PaymentEntry.deductions),

        )



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID

    ) -> Optional[PaymentEntry]:

        return db.scalar(

            select(PaymentEntry)

            .options(*self._eager())

            .where(PaymentEntry.business_id == business_id, PaymentEntry.id == entry_id)

        )



    def get_by_name(self, db: Session, business_id: uuid.UUID, name: str) -> Optional[PaymentEntry]:

        return db.scalar(

            select(PaymentEntry).where(

                PaymentEntry.business_id == business_id, PaymentEntry.name == name

            )

        )



    def next_name(self, db: Session, business_id: uuid.UUID, on: date) -> str:

        """``ACC-PAY-.YYYY.-#####``, counter scoped per tenant and year."""

        start, end = date(on.year, 1, 1), date(on.year, 12, 31)

        count = int(

            db.scalar(

                select(func.count())

                .select_from(PaymentEntry)

                .where(

                    PaymentEntry.business_id == business_id,

                    PaymentEntry.created_at >= start,

                    PaymentEntry.created_at <= end,

                )

            )

            or 0

        )

        return f"ACC-PAY-{on.year}-{count + 1:05d}"



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        payment_type: Optional[str] = None,

        party_type: Optional[str] = None,

        party: Optional[str] = None,

        from_date: Optional[date] = None,

        to_date: Optional[date] = None,

        search: Optional[str] = None,

        docstatus: Optional[int] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[PaymentEntry], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [PaymentEntry.business_id == business_id]

        if payment_type:

            conditions.append(PaymentEntry.payment_type == payment_type)

        if party_type:

            conditions.append(PaymentEntry.party_type == party_type)

        if party:

            conditions.append(PaymentEntry.party == party)

        if from_date is not None:

            conditions.append(PaymentEntry.posting_date >= from_date)

        if to_date is not None:

            conditions.append(PaymentEntry.posting_date <= to_date)

        if search:

            pattern = f"%{search}%"

            conditions.append(

                PaymentEntry.name.ilike(pattern)

                | PaymentEntry.party.ilike(pattern)

                | PaymentEntry.party_name.ilike(pattern)

                | PaymentEntry.reference_no.ilike(pattern)

            )

        if docstatus is not None:

            conditions.append(PaymentEntry.docstatus == docstatus)

        elif not include_cancelled:

            conditions.append(PaymentEntry.docstatus != 2)



        total = int(

            db.scalar(select(func.count()).select_from(PaymentEntry).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(PaymentEntry)

            .options(*self._eager())

            .where(*conditions)

            .order_by(PaymentEntry.posting_date.desc(), PaymentEntry.name.desc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, entry: PaymentEntry) -> PaymentEntry:

        db.add(entry)

        db.flush()

        return entry



    def delete(self, db: Session, entry: PaymentEntry) -> None:

        db.delete(entry)

        db.flush()

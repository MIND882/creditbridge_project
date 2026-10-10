"""Data access for AdvancePaymentLedgerEntry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.advance_payment_ledger_entry_domain.models.advance_payment_ledger_entry import AdvancePaymentLedgerEntry

from app.core.pagination import normalise_paging



__all__ = ["AdvancePaymentLedgerEntryRepository"]





class AdvancePaymentLedgerEntryRepository:

    model = AdvancePaymentLedgerEntry





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[AdvancePaymentLedgerEntry]:

        return db.scalar(

            select(AdvancePaymentLedgerEntry).where(

                AdvancePaymentLedgerEntry.business_id == business_id, AdvancePaymentLedgerEntry.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[AdvancePaymentLedgerEntry]:

        return db.scalar(

            select(AdvancePaymentLedgerEntry).where(

                AdvancePaymentLedgerEntry.business_id == business_id, AdvancePaymentLedgerEntry.name == name

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

    ) -> tuple[Sequence[AdvancePaymentLedgerEntry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [AdvancePaymentLedgerEntry.business_id == business_id]

        if not include_cancelled:

            conditions.append(AdvancePaymentLedgerEntry.docstatus != 2)

        if search:

            conditions.append(AdvancePaymentLedgerEntry.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(AdvancePaymentLedgerEntry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(AdvancePaymentLedgerEntry)

            .where(*conditions)

            .order_by(AdvancePaymentLedgerEntry.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: AdvancePaymentLedgerEntry) -> AdvancePaymentLedgerEntry:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: AdvancePaymentLedgerEntry) -> None:

        db.delete(row)

        db.flush()

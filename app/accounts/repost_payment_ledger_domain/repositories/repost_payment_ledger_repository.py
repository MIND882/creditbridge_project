"""Data access for RepostPaymentLedger. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.repost_payment_ledger_domain.models.repost_payment_ledger import RepostPaymentLedger

from app.core.pagination import normalise_paging



__all__ = ["RepostPaymentLedgerRepository"]





class RepostPaymentLedgerRepository:

    model = RepostPaymentLedger



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(RepostPaymentLedger.repost_vouchers)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[RepostPaymentLedger]:

        return db.scalar(

            select(RepostPaymentLedger).where(

                RepostPaymentLedger.business_id == business_id, RepostPaymentLedger.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[RepostPaymentLedger]:

        return db.scalar(

            select(RepostPaymentLedger).where(

                RepostPaymentLedger.business_id == business_id, RepostPaymentLedger.name == name

            ).options(*self._options())

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

    ) -> tuple[Sequence[RepostPaymentLedger], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [RepostPaymentLedger.business_id == business_id]

        if not include_cancelled:

            conditions.append(RepostPaymentLedger.docstatus != 2)

        if search:

            conditions.append(RepostPaymentLedger.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(RepostPaymentLedger).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(RepostPaymentLedger)

            .where(*conditions)

            .order_by(RepostPaymentLedger.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: RepostPaymentLedger) -> RepostPaymentLedger:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: RepostPaymentLedger) -> None:

        db.delete(row)

        db.flush()

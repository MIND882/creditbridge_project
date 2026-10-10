"""Data access for CashierClosing. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.cashier_closing_domain.models.cashier_closing import CashierClosing

from app.core.pagination import normalise_paging



__all__ = ["CashierClosingRepository"]





class CashierClosingRepository:

    model = CashierClosing



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(CashierClosing.payments)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CashierClosing]:

        return db.scalar(

            select(CashierClosing).where(

                CashierClosing.business_id == business_id, CashierClosing.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[CashierClosing]:

        return db.scalar(

            select(CashierClosing).where(

                CashierClosing.business_id == business_id, CashierClosing.name == name

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

    ) -> tuple[Sequence[CashierClosing], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [CashierClosing.business_id == business_id]

        if not include_cancelled:

            conditions.append(CashierClosing.docstatus != 2)

        if search:

            conditions.append(CashierClosing.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(CashierClosing).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(CashierClosing)

            .where(*conditions)

            .order_by(CashierClosing.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: CashierClosing) -> CashierClosing:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: CashierClosing) -> None:

        db.delete(row)

        db.flush()

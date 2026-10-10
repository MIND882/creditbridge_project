"""Data access for ProcessPeriodClosingVoucher. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.process_period_closing_voucher_domain.models.process_period_closing_voucher import ProcessPeriodClosingVoucher

from app.core.pagination import normalise_paging



__all__ = ["ProcessPeriodClosingVoucherRepository"]





class ProcessPeriodClosingVoucherRepository:

    model = ProcessPeriodClosingVoucher



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(ProcessPeriodClosingVoucher.normal_balances), selectinload(ProcessPeriodClosingVoucher.z_opening_balances)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProcessPeriodClosingVoucher]:

        return db.scalar(

            select(ProcessPeriodClosingVoucher).where(

                ProcessPeriodClosingVoucher.business_id == business_id, ProcessPeriodClosingVoucher.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProcessPeriodClosingVoucher]:

        return db.scalar(

            select(ProcessPeriodClosingVoucher).where(

                ProcessPeriodClosingVoucher.business_id == business_id, ProcessPeriodClosingVoucher.name == name

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

    ) -> tuple[Sequence[ProcessPeriodClosingVoucher], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProcessPeriodClosingVoucher.business_id == business_id]

        if not include_cancelled:

            conditions.append(ProcessPeriodClosingVoucher.docstatus != 2)

        if search:

            conditions.append(ProcessPeriodClosingVoucher.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ProcessPeriodClosingVoucher).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProcessPeriodClosingVoucher)

            .where(*conditions)

            .order_by(ProcessPeriodClosingVoucher.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: ProcessPeriodClosingVoucher) -> ProcessPeriodClosingVoucher:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ProcessPeriodClosingVoucher) -> None:

        db.delete(row)

        db.flush()

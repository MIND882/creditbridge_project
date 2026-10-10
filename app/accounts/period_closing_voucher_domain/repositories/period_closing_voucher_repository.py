"""Data access for PeriodClosingVoucher. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.period_closing_voucher_domain.models.period_closing_voucher import PeriodClosingVoucher

from app.core.pagination import normalise_paging



__all__ = ["PeriodClosingVoucherRepository"]





class PeriodClosingVoucherRepository:

    model = PeriodClosingVoucher





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PeriodClosingVoucher]:

        return db.scalar(

            select(PeriodClosingVoucher).where(

                PeriodClosingVoucher.business_id == business_id, PeriodClosingVoucher.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PeriodClosingVoucher]:

        return db.scalar(

            select(PeriodClosingVoucher).where(

                PeriodClosingVoucher.business_id == business_id, PeriodClosingVoucher.name == name

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

    ) -> tuple[Sequence[PeriodClosingVoucher], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PeriodClosingVoucher.business_id == business_id]

        if not include_cancelled:

            conditions.append(PeriodClosingVoucher.docstatus != 2)

        if search:

            conditions.append(PeriodClosingVoucher.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PeriodClosingVoucher).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PeriodClosingVoucher)

            .where(*conditions)

            .order_by(PeriodClosingVoucher.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: PeriodClosingVoucher) -> PeriodClosingVoucher:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PeriodClosingVoucher) -> None:

        db.delete(row)

        db.flush()

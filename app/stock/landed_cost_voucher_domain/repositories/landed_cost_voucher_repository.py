"""Data access for LandedCostVoucher. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.landed_cost_voucher_domain.models.landed_cost_voucher import LandedCostVoucher

from app.core.pagination import normalise_paging



__all__ = ["LandedCostVoucherRepository"]





class LandedCostVoucherRepository:

    model = LandedCostVoucher





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LandedCostVoucher]:

        return db.scalar(

            select(LandedCostVoucher).where(

                LandedCostVoucher.business_id == business_id, LandedCostVoucher.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[LandedCostVoucher]:

        return db.scalar(

            select(LandedCostVoucher).where(

                LandedCostVoucher.business_id == business_id, LandedCostVoucher.name == name

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

    ) -> tuple[Sequence[LandedCostVoucher], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LandedCostVoucher.business_id == business_id]

        if not include_cancelled:

            conditions.append(LandedCostVoucher.docstatus != 2)

        if search:

            conditions.append(LandedCostVoucher.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(LandedCostVoucher).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LandedCostVoucher)

            .where(*conditions)

            .order_by(LandedCostVoucher.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: LandedCostVoucher) -> LandedCostVoucher:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: LandedCostVoucher) -> None:

        db.delete(row)

        db.flush()

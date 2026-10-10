"""Data access for BankClearanceDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_clearance_detail_domain.models.bank_clearance_detail import BankClearanceDetail

from app.core.pagination import normalise_paging



__all__ = ["BankClearanceDetailRepository"]





class BankClearanceDetailRepository:

    model = BankClearanceDetail



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BankClearanceDetail]:

        return db.scalar(

            select(BankClearanceDetail).where(BankClearanceDetail.business_id == business_id, BankClearanceDetail.id == row_id)

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BankClearanceDetail], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [BankClearanceDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(BankClearanceDetail.parent_id == parent_id)



        total = int(db.scalar(select(func.count()).select_from(BankClearanceDetail).where(*conditions)) or 0)

        rows = db.scalars(

            select(BankClearanceDetail).where(*conditions).order_by(BankClearanceDetail.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total

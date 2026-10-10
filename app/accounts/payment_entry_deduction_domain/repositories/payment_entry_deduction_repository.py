"""Data access for PaymentEntryDeduction. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_entry_deduction_domain.models.payment_entry_deduction import PaymentEntryDeduction

from app.core.pagination import normalise_paging



__all__ = ["PaymentEntryDeductionRepository"]





class PaymentEntryDeductionRepository:

    model = PaymentEntryDeduction



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[PaymentEntryDeduction]:

        return db.scalar(select(PaymentEntryDeduction).where(PaymentEntryDeduction.business_id == business_id, PaymentEntryDeduction.id == row_id))



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PaymentEntryDeduction], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentEntryDeduction.business_id == business_id]

        if parent_id is not None:

            conditions.append(PaymentEntryDeduction.parent_id == parent_id)

        total = int(db.scalar(select(func.count()).select_from(PaymentEntryDeduction).where(*conditions)) or 0)

        rows = db.scalars(

            select(PaymentEntryDeduction).where(*conditions).order_by(PaymentEntryDeduction.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total

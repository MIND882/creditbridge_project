"""Data access for PaymentEntryReference. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_entry_reference_domain.models.payment_entry_reference import PaymentEntryReference

from app.core.pagination import normalise_paging



__all__ = ["PaymentEntryReferenceRepository"]





class PaymentEntryReferenceRepository:

    model = PaymentEntryReference



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[PaymentEntryReference]:

        return db.scalar(select(PaymentEntryReference).where(PaymentEntryReference.business_id == business_id, PaymentEntryReference.id == row_id))



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PaymentEntryReference], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentEntryReference.business_id == business_id]

        if parent_id is not None:

            conditions.append(PaymentEntryReference.parent_id == parent_id)

        total = int(db.scalar(select(func.count()).select_from(PaymentEntryReference).where(*conditions)) or 0)

        rows = db.scalars(

            select(PaymentEntryReference).where(*conditions).order_by(PaymentEntryReference.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total

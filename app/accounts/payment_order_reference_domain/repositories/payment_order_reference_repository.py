"""Data access for PaymentOrderReference. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_order_reference_domain.models.payment_order_reference import PaymentOrderReference

from app.core.pagination import normalise_paging



__all__ = ["PaymentOrderReferenceRepository"]





class PaymentOrderReferenceRepository:

    model = PaymentOrderReference





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PaymentOrderReference]:

        return db.scalar(

            select(PaymentOrderReference).where(

                PaymentOrderReference.business_id == business_id, PaymentOrderReference.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PaymentOrderReference], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentOrderReference.business_id == business_id]

        if parent_id is not None:

            conditions.append(PaymentOrderReference.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PaymentOrderReference).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PaymentOrderReference)

            .where(*conditions)

            .order_by(PaymentOrderReference.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



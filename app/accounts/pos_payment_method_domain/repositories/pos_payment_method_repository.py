"""Data access for POSPaymentMethod. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_payment_method_domain.models.pos_payment_method import POSPaymentMethod

from app.core.pagination import normalise_paging



__all__ = ["POSPaymentMethodRepository"]





class POSPaymentMethodRepository:

    model = POSPaymentMethod





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSPaymentMethod]:

        return db.scalar(

            select(POSPaymentMethod).where(

                POSPaymentMethod.business_id == business_id, POSPaymentMethod.id == row_id

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

    ) -> tuple[Sequence[POSPaymentMethod], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSPaymentMethod.business_id == business_id]

        if parent_id is not None:

            conditions.append(POSPaymentMethod.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(POSPaymentMethod).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSPaymentMethod)

            .where(*conditions)

            .order_by(POSPaymentMethod.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



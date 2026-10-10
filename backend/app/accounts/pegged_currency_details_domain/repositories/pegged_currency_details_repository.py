"""Data access for PeggedCurrencyDetails. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pegged_currency_details_domain.models.pegged_currency_details import PeggedCurrencyDetails

from app.core.pagination import normalise_paging



__all__ = ["PeggedCurrencyDetailsRepository"]





class PeggedCurrencyDetailsRepository:

    model = PeggedCurrencyDetails





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PeggedCurrencyDetails]:

        return db.scalar(

            select(PeggedCurrencyDetails).where(

                PeggedCurrencyDetails.business_id == business_id, PeggedCurrencyDetails.id == row_id

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

    ) -> tuple[Sequence[PeggedCurrencyDetails], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PeggedCurrencyDetails.business_id == business_id]

        if parent_id is not None:

            conditions.append(PeggedCurrencyDetails.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PeggedCurrencyDetails).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PeggedCurrencyDetails)

            .where(*conditions)

            .order_by(PeggedCurrencyDetails.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



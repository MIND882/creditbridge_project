"""Data access for SalesPartnerItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.sales_partner_item_domain.models.sales_partner_item import SalesPartnerItem

from app.core.pagination import normalise_paging



__all__ = ["SalesPartnerItemRepository"]





class SalesPartnerItemRepository:

    model = SalesPartnerItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesPartnerItem]:

        return db.scalar(

            select(SalesPartnerItem).where(

                SalesPartnerItem.business_id == business_id, SalesPartnerItem.id == row_id

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

    ) -> tuple[Sequence[SalesPartnerItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesPartnerItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(SalesPartnerItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SalesPartnerItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesPartnerItem)

            .where(*conditions)

            .order_by(SalesPartnerItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



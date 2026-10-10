"""Data access for CampaignItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.campaign_item_domain.models.campaign_item import CampaignItem

from app.core.pagination import normalise_paging



__all__ = ["CampaignItemRepository"]





class CampaignItemRepository:

    model = CampaignItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CampaignItem]:

        return db.scalar(

            select(CampaignItem).where(

                CampaignItem.business_id == business_id, CampaignItem.id == row_id

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

    ) -> tuple[Sequence[CampaignItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [CampaignItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(CampaignItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(CampaignItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(CampaignItem)

            .where(*conditions)

            .order_by(CampaignItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



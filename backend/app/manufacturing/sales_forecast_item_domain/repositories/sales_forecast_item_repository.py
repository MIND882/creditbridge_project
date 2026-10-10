"""Data access for SalesForecastItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.sales_forecast_item_domain.models.sales_forecast_item import SalesForecastItem

from app.core.pagination import normalise_paging



__all__ = ["SalesForecastItemRepository"]





class SalesForecastItemRepository:

    model = SalesForecastItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesForecastItem]:

        return db.scalar(

            select(SalesForecastItem).where(

                SalesForecastItem.business_id == business_id, SalesForecastItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SalesForecastItem]:

        return db.scalar(

            select(SalesForecastItem).where(

                SalesForecastItem.business_id == business_id, SalesForecastItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[SalesForecastItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesForecastItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(SalesForecastItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SalesForecastItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesForecastItem)

            .where(*conditions)

            .order_by(SalesForecastItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

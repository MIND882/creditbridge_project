"""Data access for SalesForecast. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.sales_forecast_domain.models.sales_forecast import SalesForecast

from app.core.pagination import normalise_paging



__all__ = ["SalesForecastRepository"]





class SalesForecastRepository:

    model = SalesForecast





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesForecast]:

        return db.scalar(

            select(SalesForecast).where(

                SalesForecast.business_id == business_id, SalesForecast.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SalesForecast]:

        return db.scalar(

            select(SalesForecast).where(

                SalesForecast.business_id == business_id, SalesForecast.name == name

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

    ) -> tuple[Sequence[SalesForecast], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesForecast.business_id == business_id]

        if not include_cancelled:

            conditions.append(SalesForecast.docstatus != 2)

        if search:

            conditions.append(SalesForecast.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SalesForecast).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesForecast)

            .where(*conditions)

            .order_by(SalesForecast.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SalesForecast) -> SalesForecast:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SalesForecast) -> None:

        db.delete(row)

        db.flush()

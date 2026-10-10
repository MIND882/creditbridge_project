"""Data access for PriceListCountry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.price_list_country_domain.models.price_list_country import PriceListCountry

from app.core.pagination import normalise_paging



__all__ = ["PriceListCountryRepository"]





class PriceListCountryRepository:

    model = PriceListCountry





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PriceListCountry]:

        return db.scalar(

            select(PriceListCountry).where(

                PriceListCountry.business_id == business_id, PriceListCountry.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PriceListCountry]:

        return db.scalar(

            select(PriceListCountry).where(

                PriceListCountry.business_id == business_id, PriceListCountry.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PriceListCountry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PriceListCountry.business_id == business_id]

        if parent_id is not None:

            conditions.append(PriceListCountry.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PriceListCountry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PriceListCountry)

            .where(*conditions)

            .order_by(PriceListCountry.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

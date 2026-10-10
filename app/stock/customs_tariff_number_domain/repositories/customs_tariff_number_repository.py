"""Data access for CustomsTariffNumber. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.customs_tariff_number_domain.models.customs_tariff_number import CustomsTariffNumber

from app.core.pagination import normalise_paging



__all__ = ["CustomsTariffNumberRepository"]





class CustomsTariffNumberRepository:

    model = CustomsTariffNumber





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CustomsTariffNumber]:

        return db.scalar(

            select(CustomsTariffNumber).where(

                CustomsTariffNumber.business_id == business_id, CustomsTariffNumber.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[CustomsTariffNumber]:

        return db.scalar(

            select(CustomsTariffNumber).where(

                CustomsTariffNumber.business_id == business_id, CustomsTariffNumber.name == name

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

    ) -> tuple[Sequence[CustomsTariffNumber], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [CustomsTariffNumber.business_id == business_id]

        if search:

            conditions.append(CustomsTariffNumber.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(CustomsTariffNumber).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(CustomsTariffNumber)

            .where(*conditions)

            .order_by(CustomsTariffNumber.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: CustomsTariffNumber) -> CustomsTariffNumber:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: CustomsTariffNumber) -> None:

        db.delete(row)

        db.flush()

"""Data access for SalesPartnerType. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.sales_partner_type_domain.models.sales_partner_type import SalesPartnerType

from app.core.pagination import normalise_paging



__all__ = ["SalesPartnerTypeRepository"]





class SalesPartnerTypeRepository:

    model = SalesPartnerType





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesPartnerType]:

        return db.scalar(

            select(SalesPartnerType).where(

                SalesPartnerType.business_id == business_id, SalesPartnerType.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SalesPartnerType]:

        return db.scalar(

            select(SalesPartnerType).where(

                SalesPartnerType.business_id == business_id, SalesPartnerType.name == name

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

    ) -> tuple[Sequence[SalesPartnerType], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesPartnerType.business_id == business_id]

        if search:

            conditions.append(SalesPartnerType.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SalesPartnerType).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesPartnerType)

            .where(*conditions)

            .order_by(SalesPartnerType.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SalesPartnerType) -> SalesPartnerType:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SalesPartnerType) -> None:

        db.delete(row)

        db.flush()

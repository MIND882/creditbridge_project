"""Data access for Routing. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.routing_domain.models.routing import Routing

from app.core.pagination import normalise_paging



__all__ = ["RoutingRepository"]





class RoutingRepository:

    model = Routing





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Routing]:

        return db.scalar(

            select(Routing).where(

                Routing.business_id == business_id, Routing.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Routing]:

        return db.scalar(

            select(Routing).where(

                Routing.business_id == business_id, Routing.name == name

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

    ) -> tuple[Sequence[Routing], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Routing.business_id == business_id]

        if search:

            conditions.append(Routing.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Routing).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Routing)

            .where(*conditions)

            .order_by(Routing.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Routing) -> Routing:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Routing) -> None:

        db.delete(row)

        db.flush()

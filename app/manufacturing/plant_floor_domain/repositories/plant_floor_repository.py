"""Data access for PlantFloor. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.plant_floor_domain.models.plant_floor import PlantFloor

from app.core.pagination import normalise_paging



__all__ = ["PlantFloorRepository"]





class PlantFloorRepository:

    model = PlantFloor





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PlantFloor]:

        return db.scalar(

            select(PlantFloor).where(

                PlantFloor.business_id == business_id, PlantFloor.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PlantFloor]:

        return db.scalar(

            select(PlantFloor).where(

                PlantFloor.business_id == business_id, PlantFloor.name == name

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

    ) -> tuple[Sequence[PlantFloor], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PlantFloor.business_id == business_id]

        if search:

            conditions.append(PlantFloor.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PlantFloor).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PlantFloor)

            .where(*conditions)

            .order_by(PlantFloor.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: PlantFloor) -> PlantFloor:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PlantFloor) -> None:

        db.delete(row)

        db.flush()

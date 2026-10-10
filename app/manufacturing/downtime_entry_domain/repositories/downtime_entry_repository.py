"""Data access for DowntimeEntry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.downtime_entry_domain.models.downtime_entry import DowntimeEntry

from app.core.pagination import normalise_paging



__all__ = ["DowntimeEntryRepository"]





class DowntimeEntryRepository:

    model = DowntimeEntry





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[DowntimeEntry]:

        return db.scalar(

            select(DowntimeEntry).where(

                DowntimeEntry.business_id == business_id, DowntimeEntry.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[DowntimeEntry]:

        return db.scalar(

            select(DowntimeEntry).where(

                DowntimeEntry.business_id == business_id, DowntimeEntry.name == name

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

    ) -> tuple[Sequence[DowntimeEntry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [DowntimeEntry.business_id == business_id]

        if search:

            conditions.append(DowntimeEntry.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(DowntimeEntry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(DowntimeEntry)

            .where(*conditions)

            .order_by(DowntimeEntry.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: DowntimeEntry) -> DowntimeEntry:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: DowntimeEntry) -> None:

        db.delete(row)

        db.flush()

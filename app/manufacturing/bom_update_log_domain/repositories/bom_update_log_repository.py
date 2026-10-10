"""Data access for BomUpdateLog. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_update_log_domain.models.bom_update_log import BomUpdateLog

from app.core.pagination import normalise_paging



__all__ = ["BomUpdateLogRepository"]





class BomUpdateLogRepository:

    model = BomUpdateLog





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BomUpdateLog]:

        return db.scalar(

            select(BomUpdateLog).where(

                BomUpdateLog.business_id == business_id, BomUpdateLog.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BomUpdateLog]:

        return db.scalar(

            select(BomUpdateLog).where(

                BomUpdateLog.business_id == business_id, BomUpdateLog.name == name

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

    ) -> tuple[Sequence[BomUpdateLog], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BomUpdateLog.business_id == business_id]

        if not include_cancelled:

            conditions.append(BomUpdateLog.docstatus != 2)

        if search:

            conditions.append(BomUpdateLog.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(BomUpdateLog).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BomUpdateLog)

            .where(*conditions)

            .order_by(BomUpdateLog.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: BomUpdateLog) -> BomUpdateLog:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: BomUpdateLog) -> None:

        db.delete(row)

        db.flush()

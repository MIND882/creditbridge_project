"""Data access for PackingSlip. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.packing_slip_domain.models.packing_slip import PackingSlip

from app.core.pagination import normalise_paging



__all__ = ["PackingSlipRepository"]





class PackingSlipRepository:

    model = PackingSlip





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PackingSlip]:

        return db.scalar(

            select(PackingSlip).where(

                PackingSlip.business_id == business_id, PackingSlip.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PackingSlip]:

        return db.scalar(

            select(PackingSlip).where(

                PackingSlip.business_id == business_id, PackingSlip.name == name

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

    ) -> tuple[Sequence[PackingSlip], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PackingSlip.business_id == business_id]

        if not include_cancelled:

            conditions.append(PackingSlip.docstatus != 2)

        if search:

            conditions.append(PackingSlip.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PackingSlip).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PackingSlip)

            .where(*conditions)

            .order_by(PackingSlip.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: PackingSlip) -> PackingSlip:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PackingSlip) -> None:

        db.delete(row)

        db.flush()

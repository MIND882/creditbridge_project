"""Data access for BomWebsiteOperation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_website_operation_domain.models.bom_website_operation import BomWebsiteOperation

from app.core.pagination import normalise_paging



__all__ = ["BomWebsiteOperationRepository"]





class BomWebsiteOperationRepository:

    model = BomWebsiteOperation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BomWebsiteOperation]:

        return db.scalar(

            select(BomWebsiteOperation).where(

                BomWebsiteOperation.business_id == business_id, BomWebsiteOperation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BomWebsiteOperation]:

        return db.scalar(

            select(BomWebsiteOperation).where(

                BomWebsiteOperation.business_id == business_id, BomWebsiteOperation.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BomWebsiteOperation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BomWebsiteOperation.business_id == business_id]

        if parent_id is not None:

            conditions.append(BomWebsiteOperation.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BomWebsiteOperation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BomWebsiteOperation)

            .where(*conditions)

            .order_by(BomWebsiteOperation.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

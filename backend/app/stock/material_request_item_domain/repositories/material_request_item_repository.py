"""Data access for MaterialRequestItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.material_request_item_domain.models.material_request_item import MaterialRequestItem

from app.core.pagination import normalise_paging



__all__ = ["MaterialRequestItemRepository"]





class MaterialRequestItemRepository:

    model = MaterialRequestItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[MaterialRequestItem]:

        return db.scalar(

            select(MaterialRequestItem).where(

                MaterialRequestItem.business_id == business_id, MaterialRequestItem.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[MaterialRequestItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [MaterialRequestItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(MaterialRequestItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(MaterialRequestItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(MaterialRequestItem)

            .where(*conditions)

            .order_by(MaterialRequestItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

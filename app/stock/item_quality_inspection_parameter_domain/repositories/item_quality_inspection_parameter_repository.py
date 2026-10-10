"""Data access for ItemQualityInspectionParameter. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_quality_inspection_parameter_domain.models.item_quality_inspection_parameter import ItemQualityInspectionParameter

from app.core.pagination import normalise_paging



__all__ = ["ItemQualityInspectionParameterRepository"]





class ItemQualityInspectionParameterRepository:

    model = ItemQualityInspectionParameter





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemQualityInspectionParameter]:

        return db.scalar(

            select(ItemQualityInspectionParameter).where(

                ItemQualityInspectionParameter.business_id == business_id, ItemQualityInspectionParameter.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ItemQualityInspectionParameter], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemQualityInspectionParameter.business_id == business_id]

        if parent_id is not None:

            conditions.append(ItemQualityInspectionParameter.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ItemQualityInspectionParameter).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemQualityInspectionParameter)

            .where(*conditions)

            .order_by(ItemQualityInspectionParameter.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

"""Data access for MaterialRequestPlanItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.material_request_plan_item_domain.models.material_request_plan_item import MaterialRequestPlanItem

from app.core.pagination import normalise_paging



__all__ = ["MaterialRequestPlanItemRepository"]





class MaterialRequestPlanItemRepository:

    model = MaterialRequestPlanItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[MaterialRequestPlanItem]:

        return db.scalar(

            select(MaterialRequestPlanItem).where(

                MaterialRequestPlanItem.business_id == business_id, MaterialRequestPlanItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[MaterialRequestPlanItem]:

        return db.scalar(

            select(MaterialRequestPlanItem).where(

                MaterialRequestPlanItem.business_id == business_id, MaterialRequestPlanItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[MaterialRequestPlanItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [MaterialRequestPlanItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(MaterialRequestPlanItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(MaterialRequestPlanItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(MaterialRequestPlanItem)

            .where(*conditions)

            .order_by(MaterialRequestPlanItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total

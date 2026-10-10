"""Data access for BomUpdateTool. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_update_tool_domain.models.bom_update_tool import BomUpdateTool

from app.core.pagination import normalise_paging



__all__ = ["BomUpdateToolRepository"]





class BomUpdateToolRepository:

    model = BomUpdateTool





    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[BomUpdateTool]:

        return db.scalar(

            select(BomUpdateTool).where(

                BomUpdateTool.business_id == business_id

            )

        )



    def add(self, db: Session, row: BomUpdateTool) -> BomUpdateTool:

        db.add(row)

        db.flush()

        return row

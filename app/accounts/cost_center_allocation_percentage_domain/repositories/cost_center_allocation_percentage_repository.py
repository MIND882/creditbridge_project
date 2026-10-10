"""

Data access for Cost Center Allocation Percentage.



A child table: reads are by parent, and writes go through the parent service so

``idx`` ordering and the 100% invariant stay consistent.

"""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.cost_center_allocation_percentage_domain.models.cost_center_allocation_percentage import (

    CostCenterAllocationPercentage,

)

from app.core.pagination import normalise_paging



__all__ = ["CostCenterAllocationPercentageRepository"]





class CostCenterAllocationPercentageRepository:

    model = CostCenterAllocationPercentage



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CostCenterAllocationPercentage]:

        return db.scalar(

            select(CostCenterAllocationPercentage).where(

                CostCenterAllocationPercentage.business_id == business_id,

                CostCenterAllocationPercentage.id == row_id,

            )

        )



    def list_by_parent(

        self, db: Session, business_id: uuid.UUID, parent_id: uuid.UUID

    ) -> list[CostCenterAllocationPercentage]:

        """Rows of one allocation, in ``idx`` order."""

        return list(

            db.scalars(

                select(CostCenterAllocationPercentage)

                .where(

                    CostCenterAllocationPercentage.business_id == business_id,

                    CostCenterAllocationPercentage.parent_id == parent_id,

                )

                .order_by(CostCenterAllocationPercentage.idx.asc())

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

        cost_center_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[CostCenterAllocationPercentage], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [CostCenterAllocationPercentage.business_id == business_id]

        if parent_id is not None:

            conditions.append(CostCenterAllocationPercentage.parent_id == parent_id)

        if cost_center_id is not None:

            conditions.append(CostCenterAllocationPercentage.cost_center_id == cost_center_id)



        total = int(

            db.scalar(

                select(func.count())

                .select_from(CostCenterAllocationPercentage)

                .where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(CostCenterAllocationPercentage)

            .where(*conditions)

            .order_by(CostCenterAllocationPercentage.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: CostCenterAllocationPercentage) -> CostCenterAllocationPercentage:

        db.add(row)

        db.flush()

        return row

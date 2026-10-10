"""Data access for Cost Center. Every query is scoped by ``business_id``."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.cost_center_domain.models.cost_center import CostCenter

from app.core.pagination import normalise_paging



__all__ = ["CostCenterRepository"]





class CostCenterRepository:

    model = CostCenter



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> Optional[CostCenter]:

        return db.scalar(

            select(CostCenter).where(

                CostCenter.business_id == business_id,

                CostCenter.id == cost_center_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[CostCenter]:

        return db.scalar(

            select(CostCenter).where(

                CostCenter.business_id == business_id,

                CostCenter.name == name,

            )

        )



    def find_by_number(

        self,

        db: Session,

        business_id: uuid.UUID,

        cost_center_number: str,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> Optional[CostCenter]:

        conditions = [

            CostCenter.business_id == business_id,

            CostCenter.cost_center_number == cost_center_number,

        ]

        if exclude_id is not None:

            conditions.append(CostCenter.id != exclude_id)

        return db.scalar(select(CostCenter).where(*conditions))



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        is_group: Optional[bool] = None,

        include_disabled: bool = True,

        parent_cost_center_id: Optional[uuid.UUID] = None,

        roots_only: bool = False,

    ) -> tuple[Sequence[CostCenter], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [CostCenter.business_id == business_id]

        if search:

            pattern = f"%{search}%"

            conditions.append(

                CostCenter.cost_center_name.ilike(pattern) | CostCenter.name.ilike(pattern)

            )

        if is_group is not None:

            conditions.append(CostCenter.is_group.is_(is_group))

        if not include_disabled:

            conditions.append(CostCenter.disabled.is_(False))

        if roots_only:

            conditions.append(CostCenter.parent_cost_center_id.is_(None))

        elif parent_cost_center_id is not None:

            conditions.append(CostCenter.parent_cost_center_id == parent_cost_center_id)



        total = int(

            db.scalar(select(func.count()).select_from(CostCenter).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(CostCenter)

            .where(*conditions)

            .order_by(CostCenter.cost_center_name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def list_all(self, db: Session, business_id: uuid.UUID) -> list[CostCenter]:

        return list(

            db.scalars(

                select(CostCenter)

                .where(CostCenter.business_id == business_id)

                .order_by(CostCenter.cost_center_name.asc())

            )

        )



    def list_groups(

        self, db: Session, business_id: uuid.UUID, *, search: Optional[str] = None

    ) -> list[CostCenter]:

        conditions = [

            CostCenter.business_id == business_id,

            CostCenter.is_group.is_(True),

        ]

        if search:

            conditions.append(CostCenter.cost_center_name.ilike(f"%{search}%"))

        return list(

            db.scalars(

                select(CostCenter).where(*conditions).order_by(CostCenter.cost_center_name.asc())

            )

        )



    def add(self, db: Session, cost_center: CostCenter) -> CostCenter:

        db.add(cost_center)

        db.flush()

        return cost_center



    def delete(self, db: Session, cost_center: CostCenter) -> None:

        db.delete(cost_center)

        db.flush()

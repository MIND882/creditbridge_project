"""Data access for Cost Center Allocation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.cost_center_allocation_domain.models.cost_center_allocation import (

    CostCenterAllocation,

)

from app.core.pagination import normalise_paging



__all__ = ["CostCenterAllocationRepository"]





class CostCenterAllocationRepository:

    model = CostCenterAllocation



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, allocation_id: uuid.UUID

    ) -> Optional[CostCenterAllocation]:

        """Eager-loads the child rows so serialisation does not emit N queries."""

        return db.scalar(

            select(CostCenterAllocation)

            .options(selectinload(CostCenterAllocation.allocation_percentages))

            .where(

                CostCenterAllocation.business_id == business_id,

                CostCenterAllocation.id == allocation_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[CostCenterAllocation]:

        return db.scalar(

            select(CostCenterAllocation)

            .options(selectinload(CostCenterAllocation.allocation_percentages))

            .where(

                CostCenterAllocation.business_id == business_id,

                CostCenterAllocation.name == name,

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        main_cost_center_id: Optional[uuid.UUID] = None,

        docstatus: Optional[int] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[CostCenterAllocation], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [CostCenterAllocation.business_id == business_id]

        if main_cost_center_id is not None:

            conditions.append(CostCenterAllocation.main_cost_center_id == main_cost_center_id)

        if docstatus is not None:

            conditions.append(CostCenterAllocation.docstatus == docstatus)

        elif not include_cancelled:

            # Mirrors ERPNext's ubiquitous `docstatus != 2`.

            conditions.append(CostCenterAllocation.docstatus != 2)



        total = int(

            db.scalar(

                select(func.count()).select_from(CostCenterAllocation).where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(CostCenterAllocation)

            .options(selectinload(CostCenterAllocation.allocation_percentages))

            .where(*conditions)

            .order_by(CostCenterAllocation.name.desc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """

        ``CC-ALLOC-.#####`` scoped per tenant.



        Derived from the tenant's row count rather than a shared sequence, so

        two tenants both start at 00001.

        """

        count = int(

            db.scalar(

                select(func.count())

                .select_from(CostCenterAllocation)

                .where(CostCenterAllocation.business_id == business_id)

            )

            or 0

        )

        return f"CC-ALLOC-{count + 1:05d}"



    def find_future_allocation(

        self,

        db: Session,

        business_id: uuid.UUID,

        main_cost_center_id: uuid.UUID,

        valid_from,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> Optional[CostCenterAllocation]:

        """

        Port of ``validate_backdated_allocation``'s query: the earliest

        *submitted* allocation for this main cost centre on or after

        ``valid_from``.

        """

        conditions = [

            CostCenterAllocation.business_id == business_id,

            CostCenterAllocation.main_cost_center_id == main_cost_center_id,

            CostCenterAllocation.valid_from >= valid_from,

            CostCenterAllocation.docstatus == 1,

        ]

        if exclude_id is not None:

            conditions.append(CostCenterAllocation.id != exclude_id)

        return db.scalar(

            select(CostCenterAllocation)

            .where(*conditions)

            .order_by(CostCenterAllocation.valid_from.asc())

            .limit(1)

        )



    def list_main_cost_center_ids(

        self, db: Session, business_id: uuid.UUID

    ) -> set[uuid.UUID]:

        """

        Every cost centre used as a *main* in a submitted allocation.



        Port of the ``main_cost_centers`` list built in

        ``validate_child_cost_centers``.

        """

        rows = db.scalars(

            select(CostCenterAllocation.main_cost_center_id).where(

                CostCenterAllocation.business_id == business_id,

                CostCenterAllocation.docstatus == 1,

            )

        ).all()

        return set(rows)



    def add(self, db: Session, allocation: CostCenterAllocation) -> CostCenterAllocation:

        db.add(allocation)

        db.flush()

        return allocation



    def delete(self, db: Session, allocation: CostCenterAllocation) -> None:

        db.delete(allocation)

        db.flush()

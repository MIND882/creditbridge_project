"""
Repository for Opportunity data access.

Pure data-access layer — no business logic.
"""

import uuid
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.crm.opportunity_domain.models.opportunity import Opportunity, OpportunityStatus


class OpportunityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, opportunity: Opportunity) -> Opportunity:
        self.db.add(opportunity)
        self.db.flush()
        return opportunity

    def get_by_id(
        self, opportunity_id: uuid.UUID, business_id: uuid.UUID
    ) -> Optional[Opportunity]:
        stmt = select(Opportunity).where(
            Opportunity.id == opportunity_id,
            Opportunity.business_id == business_id,
            Opportunity.is_deleted.is_(False),
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_by_lead(
        self, lead_id: uuid.UUID, business_id: uuid.UUID
    ) -> list[Opportunity]:
        stmt = select(Opportunity).where(
            Opportunity.lead_id == lead_id,
            Opportunity.business_id == business_id,
            Opportunity.is_deleted.is_(False),
        )
        return list(self.db.execute(stmt).scalars().all())

    def list_by_customer(
        self, customer_id: uuid.UUID, business_id: uuid.UUID
    ) -> list[Opportunity]:
        stmt = select(Opportunity).where(
            Opportunity.customer_id == customer_id,
            Opportunity.business_id == business_id,
            Opportunity.is_deleted.is_(False),
        )
        return list(self.db.execute(stmt).scalars().all())

    def list_by_business(
        self,
        business_id: uuid.UUID,
        *,
        status: Optional[OpportunityStatus] = None,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[list[Opportunity], int]:
        filters = [
            Opportunity.business_id == business_id,
            Opportunity.is_deleted.is_(False),
        ]
        if status is not None:
            filters.append(Opportunity.status == status)

        count_stmt = select(func.count()).select_from(Opportunity).where(*filters)
        total = self.db.execute(count_stmt).scalar_one()

        stmt = (
            select(Opportunity)
            .where(*filters)
            .order_by(Opportunity.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items = list(self.db.execute(stmt).scalars().all())
        return items, total

    def list_open_stale(
        self, business_id: uuid.UUID, stale_since
    ) -> list[Opportunity]:
        """
        Used by the auto-close scheduled job (service layer) — returns
        Opportunities in a non-terminal status that haven't been updated
        since `stale_since`.
        """
        stmt = select(Opportunity).where(
            Opportunity.business_id == business_id,
            Opportunity.status == OpportunityStatus.OPEN,
            Opportunity.updated_at < stale_since,
            Opportunity.is_deleted.is_(False),
        )
        return list(self.db.execute(stmt).scalars().all())

    def update(self, opportunity: Opportunity) -> Opportunity:
        self.db.add(opportunity)
        self.db.flush()
        return opportunity

    def soft_delete(self, opportunity: Opportunity) -> Opportunity:
        opportunity.is_deleted = True
        opportunity.deleted_at = func.now()
        self.db.add(opportunity)
        self.db.flush()
        return opportunity

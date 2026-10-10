"""


Repository Layer — LeadActivity.

Pure data-access, append-only timeline. No business rules (e.g. whether
content is required for a given activity_type is enforced at the
Pydantic/Service layer, not here).
"""

from typing import Optional, Sequence
from uuid import UUID
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crm.lead_domain.models.lead import LeadActivity, LeadActivityType


class LeadActivityRepository:

    def create(self, db: Session, activity: LeadActivity) -> LeadActivity:
        db.add(activity)
        db.flush()
        db.refresh(activity)
        return activity

    def list_by_lead(
        self,
        db: Session,
        lead_id: UUID,
        business_id: UUID,
        activity_type: Optional[LeadActivityType] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> Sequence[LeadActivity]:
        """
        Newest-first, matching ix_lead_activities_lead_created. Scoped by
        both lead_id and business_id (defense-in-depth against a lead_id
        that doesn't belong to the caller's tenant slipping through).
        """
        conditions = [
            LeadActivity.lead_id == lead_id,
            LeadActivity.business_id == business_id,
        ]
        if activity_type is not None:
            conditions.append(LeadActivity.activity_type == activity_type)

        stmt = (
            select(LeadActivity)
            .where(*conditions)
            .order_by(LeadActivity.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def get_latest(
        self,
        db: Session,
        lead_id: UUID,
        activity_type: Optional[LeadActivityType] = None,
    ) -> Optional[LeadActivity]:
        conditions = [LeadActivity.lead_id == lead_id]
        if activity_type is not None:
            conditions.append(LeadActivity.activity_type == activity_type)

        stmt = (
            select(LeadActivity)
            .where(*conditions)
            .order_by(LeadActivity.created_at.desc())
            .limit(1)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_due_next_actions(
        self,
        db: Session,
        business_id: UUID,
        due_before: datetime,
    ) -> Sequence[LeadActivity]:
        """
        Cross-lead scan for the "follow-ups due" dashboard query, hitting
        ix_lead_activities_business_next_action (partial index, WHERE
        next_action_due IS NOT NULL).
        """
        stmt = (
            select(LeadActivity)
            .where(
                LeadActivity.business_id == business_id,
                LeadActivity.next_action_due.isnot(None),
                LeadActivity.next_action_due <= due_before,
            )
            .order_by(LeadActivity.next_action_due.asc())
        )
        return db.execute(stmt).scalars().all()

    def update_next_action(
        self,
        db: Session,
        activity: LeadActivity,
        next_action_due: Optional[datetime],
    ) -> LeadActivity:
        activity.next_action_due = next_action_due
        db.flush()
        db.refresh(activity)
        return activity
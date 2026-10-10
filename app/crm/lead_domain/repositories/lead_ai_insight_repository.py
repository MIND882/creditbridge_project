"""
app/crm/repositories/lead_ai_insight_repository.py

Repository Layer — LeadAIInsight.

Pure data-access for the append-only AI insight history log. Written to
exclusively by the lead_pipeline AI agents via the Service layer -- this
repository has no awareness of which agent produced a row, only how to
store/retrieve/supersede it.
"""

from typing import Optional, Sequence
from uuid import UUID
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crm.lead_domain.models.lead import LeadAIInsight, LeadAIInsightType


class LeadAIInsightRepository:

    def create(self, db: Session, insight: LeadAIInsight) -> LeadAIInsight:
        db.add(insight)
        db.flush()
        db.refresh(insight)
        return insight

    def list_by_lead(
        self,
        db: Session,
        lead_id: UUID,
        insight_type: Optional[LeadAIInsightType] = None,
        include_superseded: bool = True,
        offset: int = 0,
        limit: int = 50,
    ) -> Sequence[LeadAIInsight]:
        """
        Newest-first history for one lead, optionally filtered to a
        single insight_type (e.g. full lead_score trend over time).
        Matches ix_lead_ai_insights_lead_type_generated.
        """
        conditions = [LeadAIInsight.lead_id == lead_id]
        if insight_type is not None:
            conditions.append(LeadAIInsight.insight_type == insight_type)
        if not include_superseded:
            conditions.append(LeadAIInsight.superseded_at.is_(None))

        stmt = (
            select(LeadAIInsight)
            .where(*conditions)
            .order_by(LeadAIInsight.generated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def get_latest(
        self,
        db: Session,
        lead_id: UUID,
        insight_type: LeadAIInsightType,
    ) -> Optional[LeadAIInsight]:
        """
        Returns the current (non-superseded) insight of a given type for
        a lead, hitting the partial index ix_lead_ai_insights_current
        (WHERE superseded_at IS NULL).
        """
        stmt = (
            select(LeadAIInsight)
            .where(
                LeadAIInsight.lead_id == lead_id,
                LeadAIInsight.insight_type == insight_type,
                LeadAIInsight.superseded_at.is_(None),
            )
            .order_by(LeadAIInsight.generated_at.desc())
            .limit(1)
        )
        return db.execute(stmt).scalar_one_or_none()

    def mark_superseded(
        self,
        db: Session,
        insight: LeadAIInsight,
        superseded_at: datetime,
    ) -> LeadAIInsight:
        """
        Marks a prior insight as no longer current when a recurring agent
        produces a fresh one of the same type. Caller (Service layer) is
        responsible for calling this before/alongside create() for the
        new insight, so exactly one "current" row exists per
        (lead_id, insight_type) at a time.
        """
        insight.superseded_at = superseded_at
        db.flush()
        db.refresh(insight)
        return insight

    def supersede_current(
        self,
        db: Session,
        lead_id: UUID,
        insight_type: LeadAIInsightType,
        superseded_at: datetime,
    ) -> Optional[LeadAIInsight]:
        """
        Convenience combining get_latest() + mark_superseded() for the
        common Service-layer pattern: "before writing a new insight of
        this type, supersede whatever is currently marked current."
        Returns the superseded row, or None if there was no current row.
        """
        current = self.get_latest(db, lead_id, insight_type)
        if current is None:
            return None
        return self.mark_superseded(db, current, superseded_at)
    
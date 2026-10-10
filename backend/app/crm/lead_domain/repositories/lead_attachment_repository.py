"""


Repository Layer — LeadAttachment.

Pure data-access. Storage I/O (writing/deleting the actual file at
storage_url) is explicitly out of scope here -- this repository only
manages the database row. Orchestrating "delete DB row AND delete
storage object, in the correct order" is a Service-layer responsibility
(LeadAttachmentService), per the frozen spec.
"""

from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.crm.lead_domain.models.lead import LeadAttachment


class LeadAttachmentRepository:

    def create(self, db: Session, attachment: LeadAttachment) -> LeadAttachment:
        db.add(attachment)
        db.flush()
        db.refresh(attachment)
        return attachment

    def get_by_id(
        self,
        db: Session,
        attachment_id: UUID,
        lead_id: UUID,
        business_id: UUID,
    ) -> Optional[LeadAttachment]:
        stmt = select(LeadAttachment).where(
            LeadAttachment.id == attachment_id,
            LeadAttachment.lead_id == lead_id,
            LeadAttachment.business_id == business_id,
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_by_lead(
        self,
        db: Session,
        lead_id: UUID,
        business_id: UUID,
        category: Optional[str] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> Sequence[LeadAttachment]:
        conditions = [
            LeadAttachment.lead_id == lead_id,
            LeadAttachment.business_id == business_id,
        ]
        if category is not None:
            conditions.append(LeadAttachment.category == category)

        stmt = (
            select(LeadAttachment)
            .where(*conditions)
            .order_by(LeadAttachment.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def count_by_lead(self, db: Session, lead_id: UUID) -> int:
        """
        Supports the Service-layer enforcement of the "max attachments
        per lead" soft cap from the frozen spec, without requiring the
        caller to fetch the full list just to count it.
        """
        from sqlalchemy import func
        stmt = select(func.count()).select_from(LeadAttachment).where(
            LeadAttachment.lead_id == lead_id
        )
        return db.execute(stmt).scalar_one()

    def delete(self, db: Session, attachment: LeadAttachment) -> None:
        """
        Hard delete, per frozen spec (LeadAttachment has no soft-delete
        semantics). Only removes the DB row -- storage cleanup is a
        separate Service-layer step, ordered so a failed storage delete
        doesn't leave a dangling DB row silently (per Stage 1 doc note).
        """
        db.delete(attachment)
        db.flush()
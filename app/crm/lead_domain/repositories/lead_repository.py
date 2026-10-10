"""
app/crm/repositories/lead_repository.py

YE file CRM Lead module ki repository layer hai .

iS FILE KA SIRF EK KAAM HAI.

DATABASE SE DATA LENA AUR DATABASE ME DATA SAVE KARNA.

ISME SIRF SQLALCHEMY QUERIES HONGI.

JAISE:
- LEAD CREATE KARNA 
- LEAD FETCH KARNA
- LEAD UPDATE KARNA
- LEAD DELETE[SOFT DELETE] KARNA
- LEAD LIST KARNA

IS FILE ME KABHI NAHI HOGA:
❌ BUSINESS LOGIC
❌ DATA VALIDATION
❌ AI LOGIC
❌ EVENT PUBLISHING
❌ AI CODE 
❌ HTTP RESPONSE

YE SAB SERVICE LAYER KA KAAM HAI.

------------------------------------------------------------

TRANSACTION RULE

REPOSITORY KABHI COMMIT() YA ROLLBACK() NHI KAREGI.

REPOSITORY SIRF:

- ADD()
- UPDATE()
- DELETE()
- FLUSH()

JAISE DATABASE OPERATION KAREGI.

FINAL DECISION KI DATA DATABSE ME PERMANENTLY SAVE HOGA YA NHI 
YE SERVICE LAYER KAREGI.

REASON:

EK SERVICE EK SATH MULTIPLE REPOSITORIES USE KAR SAKTI HAI .

EXAMPLE:

CREATE LEAD 
        |
ADD ACTIVITY
        |
GENERATE AI INSIGHT
        |
UPLOAD ATTACHMENT
        |
AGAR ISME SE KOI BHI STEP FAIL HO JAYE,
TO SERVICE LAYER POORI TRANSACTION ROLLBACK KAR DEGI.

ISLIYE COMMIT() KA CONTROL HAMESHA SERVICE LAYER KE PAAS RAHEGA,
REPOSIOTRY KE PASS NAHI. 
"""

from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.crm.lead_domain.models.lead import Lead, LeadStatus, LeadQualificationStatus, LeadSource

class LeadRepository:
    def create( self, db:Session, lead: Lead) -> Lead:
        """Persist a new Lead.
        The Service layer is responsible for preparing all business and
        server-owned fields before calling this method.
        The Repository performs database persistence only.
        """
        db.add(lead)
        db.flush()
        db.refresh(lead)
        return lead

    def get_by_id(
      self, 
      db: Session, 
      lead_id: UUID,
      business_id: UUID,
      include_deleted: bool =False
    ) -> Optional[Lead]:
        stmt = select(Lead).where(
            Lead.id == lead_id,
            Lead.business_id == business_id,
        )
        if not include_deleted:
            stmt = stmt.where(Lead.is_deleted.is_(False))
        return db.execute(stmt).scalar_one_or_none()
    
    def list(
        self,
        db: Session,
        business_id: UUID,
        status: Optional[LeadStatus] = None,
        qualification_status: Optional[LeadQualificationStatus] = None,
        source: Optional[LeadSource] = None,
        lead_owner_id: Optional[UUID] = None,
        ca_partner_id: Optional[UUID] = None,
        include_deleted: bool = False,
        offset: int = 0,
        limit: int = 50,
    ) -> tuple[Sequence[Lead], int]:
        """
        Filtered, paginated list. Filters map directly to the composite/
        partial indexes defined in the frozen migration
        (ix_leads_business_status, ix_leads_business_qualification, etc.)
        so these predicates hit an index, not a sequential scan.

        Returns (items, total_count).
        """
        conditions = [Lead.business_id == business_id]
        if not include_deleted:
            conditions.append(Lead.is_deleted.is_(False))
        if status is not None:
            conditions.append(Lead.status == status)
        if qualification_status is not None:
            conditions.append(Lead.qualification_status == qualification_status)
        if source is not None:
            conditions.append(Lead.source == source)
        if lead_owner_id is not None:
            conditions.append(Lead.lead_owner_id == lead_owner_id)
        if ca_partner_id is not None:
            conditions.append(Lead.ca_partner_id == ca_partner_id)

        count_stmt = select(func.count()).select_from(Lead).where(*conditions)
        total = db.execute(count_stmt).scalar_one()

        list_stmt = (
            select(Lead)
            .where(*conditions)
            .order_by(Lead.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        items = db.execute(list_stmt).scalars().all()

        return items, total

    def update(self, db: Session, lead: Lead, update_data: dict) -> Lead:
        """
        Apply a dict of already-validated field changes to an existing
        Lead instance. Caller owns validation (Pydantic LeadUpdate) and
        any cross-field business rules -- this method only assigns and
        flushes.
        """
        for field, value in update_data.items():
            setattr(lead, field, value)
        db.flush()
        db.refresh(lead)
        return lead

    def soft_delete(self, db: Session, lead: Lead, deleted_at) -> Lead:
        lead.is_deleted = True
        lead.deleted_at = deleted_at
        db.flush()
        db.refresh(lead)
        return lead

    def restore(self, db: Session, lead: Lead) -> Lead:
        lead.is_deleted = False
        lead.deleted_at = None
        db.flush()
        db.refresh(lead)
        return lead

    def assign_owner(self, db: Session, lead: Lead, lead_owner_id: Optional[UUID]) -> Lead:
        """
        lead_owner_id may be explicitly set to None to reassign ownership
        back to the business account itself, per the nullable-owner
        semantics from the frozen spec.
        """
        lead.lead_owner_id = lead_owner_id
        db.flush()
        db.refresh(lead)
        return lead

    def change_status(self, db: Session, lead: Lead, new_status: LeadStatus) -> Lead:
        """
        Raw status assignment only. Legality of the transition (e.g.
        cannot revert Converted -> Lead) is a Service-layer business
        rule, not a repository concern.
        """
        lead.status = new_status
        db.flush()
        db.refresh(lead)
        return lead

    def mark_duplicate(self, db: Session, lead: Lead, duplicate_of_lead_id: UUID) -> Lead:
        lead.duplicate_of_lead_id = duplicate_of_lead_id
        db.flush()
        db.refresh(lead)
        return lead

    def increment_attachment_count(self, db: Session, lead: Lead, delta: int = 1) -> Lead:
        """
        Supports LeadAttachmentRepository callers (via the Service layer)
        keeping the denormalized counter on Lead in sync without each
        caller reaching into Lead's internals directly.
        """
        lead.attachment_count = max(0, (lead.attachment_count or 0) + delta)
        db.flush()
        return lead

    def increment_notes_count(self, db: Session, lead: Lead, delta: int = 1) -> Lead:
        lead.notes_count = max(0, (lead.notes_count or 0) + delta)
        db.flush()
        return lead

    def touch_last_activity(self, db: Session, lead: Lead, timestamp) -> Lead:
        lead.last_activity_at = timestamp
        db.flush()
        return lead
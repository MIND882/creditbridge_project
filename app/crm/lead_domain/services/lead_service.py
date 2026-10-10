"""
Lead Service Layer.

ye file CRM Modules KA BUSINESS LOGIC HANDLE KARTI HAI.

RESPONSIBILITIES:
- BUSINESS WORKFLOW MANAGE KARNA
- REPOSITORIES KO CALL KARNA
- TRANSACTION (COMMIT/ ROLLBACK) HANDLE KARNA

YE FILE:
- SQL DIREACTLY NHI LIKHATI.
- DATABASE  KO DIRECTLY ACCESS NHI KARTI.
- SIRF REPOSITORY KE THROUGH HI DATA SAVE YA READ KARTI HAI.

REFERENCE:
- ERPNext LEAD WORKFLOW
- CreditBridge Lead specification

Stage 5 Refactor:
- Repeated commit/rollback code ko _transaction() me move kiya.
- Repeated activity creation code ko _record_activity() me move kiya.
- Unused LeadAttachmentRepository remove kiya.
- Future AI integration ke liye TODO(Stage 7) placeholders add kiye.

No business logic was changed.
Only code readability and maintainability were improved. 
"""

from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy.orm import Session

from app.crm.lead_domain.models.lead import (
    Lead,
    LeadActivity,
    LeadActivityActorType,
    LeadActivityType,
    LeadStatus,
)
from app.crm.lead_domain.repositories.lead_repository import LeadRepository
from app.crm.lead_domain.repositories.lead_activity_repository import LeadActivityRepository
from app.crm.lead_domain.repositories.lead_ai_insight_repository import LeadAIInsightRepository
from app.crm.lead_domain.schemas.lead import (
    LeadActivityCreate,
    LeadCreate,
    LeadMarkDuplicateRequest,
    LeadQualifyRequest,
    LeadUpdate,
)

# ─────────────────────────────────────────────────────────────────────────────
# Domain exceptions
#
# HTTP-agnostic on purpose -- the API layer (Stage 6) maps these to status
# codes. The Service layer must not know about FastAPI/HTTP.
# ─────────────────────────────────────────────────────────────────────────────

class LeadServiceError(Exception):
    """base class for all lead service domain errors."""


class LeadNotFoundError(LeadServiceError):
       def __init__(self, lead_id: UUID):
             super().__init__(f"Lead {lead_id} not found.")
             self.lead_id = lead_id

class InvalidStatusTransitionError(LeadServiceError):
      def __init__(self, current: LeadStatus, target: LeadStatus):
            super().__init__(f"Cannot transition Lead status from'{current.value}' to '{target.value}' .")
            self.current =current
            self.target = target

class LeadNameGenerationError(LeadServiceError):
    """
    Last-resort safety net. LeadCreate's XOR validator (first_name OR
    company_name) should make this unreachable in practice, mirroring
    ERPNext's own belt-and-suspenders throw in set_lead_name().
    """


# ─────────────────────────────────────────────────────────────────────────────
# Status transition map
#
# Encodes which status changes are legal, replacing ERPNext's drift-prone
# pattern (status could silently go stale relative to linked document
# reality) with an explicit, enforced state machine. CONVERTED is
# deliberately unreachable via change_status() -- it is only ever set by
# the future convert() workflow once Opportunity exists, atomically with
# converted_opportunity_id.
# ─────────────────────────────────────────────────────────────────────────────

_ALLOWED_STATUS_TRANSITIONS: dict[LeadStatus, set[LeadStatus]] = {
    LeadStatus.LEAD: {LeadStatus.OPEN, LeadStatus.REPLIED, LeadStatus.DO_NOT_CONTACT},
    LeadStatus.OPEN: {
        LeadStatus.REPLIED, LeadStatus.INTERESTED, LeadStatus.DO_NOT_CONTACT,
    },
    LeadStatus.REPLIED: {
        LeadStatus.INTERESTED, LeadStatus.DO_NOT_CONTACT,
    },
    LeadStatus.INTERESTED: {LeadStatus.DO_NOT_CONTACT},
    LeadStatus.LOST_QUOTATION: {LeadStatus.INTERESTED, LeadStatus.DO_NOT_CONTACT},
    # OPPORTUNITY, QUOTATION, CONVERTED are set exclusively by the future
    # conversion pipeline, never via generic change_status().
    LeadStatus.OPPORTUNITY: set(),
    LeadStatus.QUOTATION: set(),
    LeadStatus.CONVERTED: set(),       # terminal
    LeadStatus.DO_NOT_CONTACT: set(),  # terminal
}


class LeadService:
    """
    Orchestrates Lead business workflow across repositories. Holds no
    per-request state, only repository references -- safe to reuse
    across requests.
    """

    def __init__(
        self,
        lead_repository: LeadRepository,
        activity_repository: LeadActivityRepository,
        insight_repository: LeadAIInsightRepository,
    ):
        self._leads = lead_repository
        self._activities = activity_repository
        # Not yet read or written by any method in this stage.
        # LeadAIInsight rows are produced by the Stage 7 agent layer
        # (lead_scorer_node, lead_business_size_estimator_node, etc.);
        # LeadService is expected to gain a sync method then (reading the
        # latest insight to refresh Lead.ai_lead_score). Kept as a
        # constructor dependency now so that call-site wiring doesn't
        # change when Stage 7 lands.
        self._insights = insight_repository

    # ─────────────────────────────────────────────────────────────────
    # Transaction boundary
    # ─────────────────────────────────────────────────────────────────

    @contextmanager
    def _transaction(self, db: Session):
        """
        The single place this Service commits or rolls back. Repositories
        only flush; everything inside this block either all lands or all
        rolls back together.
        """
        try:
            yield
        except Exception:
            db.rollback()
            raise
        else:
            db.commit()

    # ─────────────────────────────────────────────────────────────────
    # Create
    # ─────────────────────────────────────────────────────────────────

    def create_lead(
        self,
        db: Session,
        business_id: UUID,
        actor_id: Optional[UUID],
        payload: LeadCreate,
    ) -> Lead:
        """
        Lead creation workflow (frozen, 10 steps):

          1. business_id read from authenticated context (caller-supplied
             here -- resolving it from the JWT is the API layer's job).
          2. Check duplicate Lead (placeholder).
          3. Prepare server-owned fields.
          4. Generate lead_name.
          5. Set default Lead status.
          6. Create Lead via Repository.
          7. Create initial LeadActivity.
          8. Trigger AI enrichment pipeline (placeholder call only).
          9. Commit transaction.
          10. Return created Lead.
        """
        with self._transaction(db):
            # Step 2
            # TODO(Stage 7): real fuzzy duplicate detection lives in
            # lead_dedup_node -- see _check_duplicate_lead().
            self._check_duplicate_lead(db, business_id, payload)

            # Steps 3-5
            lead_name = self._compute_lead_name(
                first_name=payload.first_name,
                middle_name=payload.middle_name,
                last_name=payload.last_name,
                company_name=payload.company_name,
                email=payload.email,
            )
            lead = Lead(
                business_id=business_id,
                lead_owner_id=payload.lead_owner_id,
                first_name=payload.first_name,
                middle_name=payload.middle_name,
                last_name=payload.last_name,
                lead_name=lead_name,
                company_name=payload.company_name,
                title=payload.company_name or lead_name,
                gender=payload.gender,
                email=payload.email,
                phone=payload.phone,
                mobile_no=payload.mobile_no,
                whatsapp_no=payload.whatsapp_no,
                website=payload.website,
                city=payload.city,
                state=payload.state,
                country=payload.country,
                industry=payload.industry,
                business_type=payload.business_type,
                no_of_employees=payload.no_of_employees,
                declared_annual_revenue=payload.declared_annual_revenue,
                job_title=payload.job_title,
                lead_type=payload.lead_type,
                source=payload.source,
                ca_partner_id=payload.ca_partner_id,
                utm_source=payload.utm_source,
                utm_medium=payload.utm_medium,
                utm_campaign=payload.utm_campaign,
                utm_content=payload.utm_content,
                pan=payload.pan,
                gstin=payload.gstin,
                status=LeadStatus.LEAD,  # step 5 -- always the default on create
                created_by=actor_id,
            )

            # Step 6
            lead = self._leads.create(db, lead)

            # Step 7 -- initial timeline entry, always system-generated
            # regardless of who initiated the request.
            self._record_activity(
                db, lead,
                activity_type=LeadActivityType.STATUS_CHANGE,
                actor_id=actor_id,
                content=f"Lead created (source: {payload.source.value}).",
                metadata={"old_status": None, "new_status": LeadStatus.LEAD.value},
                actor_type=LeadActivityActorType.SYSTEM,
            )
            self._leads.touch_last_activity(db, lead, datetime.now(timezone.utc))

            # Step 8
            # TODO(Stage 7): publish `lead.created` to the lead_events
            # stream; consumed by lead_enricher_node, lead_dedup_node,
            # lead_scorer_node.
            self._trigger_ai_enrichment(lead)

        # Step 9 committed inside the context manager above.
        # Step 10 -- commit() expires instance attributes by default
        # (expire_on_commit=True), so refresh here to hand the caller a
        # fully-loaded object to serialize into LeadResponse.
        db.refresh(lead)
        return lead

    # ─────────────────────────────────────────────────────────────────
    # Read
    # ─────────────────────────────────────────────────────────────────

    def get_lead(self, db: Session, lead_id: UUID, business_id: UUID) -> Lead:
        lead = self._leads.get_by_id(db, lead_id, business_id)
        if lead is None:
            raise LeadNotFoundError(lead_id)
        return lead

    def list_leads(
        self,
        db: Session,
        business_id: UUID,
        **filters,
    ) -> tuple[Sequence[Lead], int]:
        """Thin pass-through to LeadRepository.list(); filters forwarded as-is."""
        return self._leads.list(db, business_id=business_id, **filters)

    # ─────────────────────────────────────────────────────────────────
    # Update
    # ─────────────────────────────────────────────────────────────────

    def update_lead(
        self,
        db: Session,
        lead_id: UUID,
        business_id: UUID,
        actor_id: Optional[UUID],
        payload: LeadUpdate,
    ) -> Lead:
        lead = self.get_lead(db, lead_id, business_id)

        update_data = payload.model_dump(exclude_unset=True)
        update_data["updated_by"] = actor_id

        # Recompute lead_name/title if any name-source field changed, so
        # the cascade stays consistent after a PATCH the same way it's
        # set on create (mirrors ERPNext's set_full_name/set_lead_name).
        name_fields = {"first_name", "middle_name", "last_name", "company_name"}
        if name_fields & update_data.keys():
            company_name = update_data.get("company_name", lead.company_name)
            new_lead_name = self._compute_lead_name(
                first_name=update_data.get("first_name", lead.first_name),
                middle_name=update_data.get("middle_name", lead.middle_name),
                last_name=update_data.get("last_name", lead.last_name),
                company_name=company_name,
                email=update_data.get("email", lead.email),
            )
            update_data["lead_name"] = new_lead_name
            update_data["title"] = company_name or new_lead_name

        with self._transaction(db):
            lead = self._leads.update(db, lead, update_data)

        db.refresh(lead)
        return lead

    # ─────────────────────────────────────────────────────────────────
    # Status / lifecycle
    # ─────────────────────────────────────────────────────────────────

    def change_status(
        self,
        db: Session,
        lead_id: UUID,
        business_id: UUID,
        actor_id: Optional[UUID],
        new_status: LeadStatus,
    ) -> Lead:
        lead = self.get_lead(db, lead_id, business_id)
        current_status = lead.status

        if new_status == current_status:
            return lead  # no-op, not an error

        allowed = _ALLOWED_STATUS_TRANSITIONS.get(current_status, set())
        if new_status not in allowed:
            raise InvalidStatusTransitionError(current_status, new_status)

        with self._transaction(db):
            lead = self._leads.change_status(db, lead, new_status)
            self._record_activity(
                db, lead,
                activity_type=LeadActivityType.STATUS_CHANGE,
                actor_id=actor_id,
                content=f"Status changed from '{current_status.value}' to '{new_status.value}'.",
                metadata={"old_status": current_status.value, "new_status": new_status.value},
            )
            self._leads.touch_last_activity(db, lead, datetime.now(timezone.utc))

        db.refresh(lead)
        return lead

    def qualify_lead(
        self,
        db: Session,
        lead_id: UUID,
        business_id: UUID,
        actor_id: Optional[UUID],
        payload: LeadQualifyRequest,
    ) -> Lead:
        lead = self.get_lead(db, lead_id, business_id)

        with self._transaction(db):
            lead = self._leads.update(
                db,
                lead,
                {
                    "qualification_status": payload.qualification_status,
                    "qualified_by": payload.qualified_by,
                    "qualified_on": payload.qualified_on,
                    "updated_by": actor_id,
                },
            )
            self._record_activity(
                db, lead,
                activity_type=LeadActivityType.STATUS_CHANGE,
                actor_id=actor_id,
                content=f"Qualification status set to '{payload.qualification_status.value}'.",
                metadata={"qualification_status": payload.qualification_status.value},
            )
            self._leads.touch_last_activity(db, lead, datetime.now(timezone.utc))

            # TODO(Stage 7): lead_scorer_node re-runs on `lead.qualified`
            # per the frozen event catalog -- qualification is a strong
            # scoring feature.
            self._trigger_ai_enrichment(lead)

        db.refresh(lead)
        return lead

    def mark_duplicate(
        self,
        db: Session,
        lead_id: UUID,
        business_id: UUID,
        actor_id: Optional[UUID],
        payload: LeadMarkDuplicateRequest,
    ) -> Lead:
        lead = self.get_lead(db, lead_id, business_id)

        # Confirm the target exists in the same tenant before linking --
        # an integrity check, not a business rule.
        duplicate_target = self._leads.get_by_id(
            db, payload.duplicate_of_lead_id, business_id, include_deleted=True
        )
        if duplicate_target is None:
            raise LeadNotFoundError(payload.duplicate_of_lead_id)

        with self._transaction(db):
            lead = self._leads.mark_duplicate(db, lead, payload.duplicate_of_lead_id)
            self._record_activity(
                db, lead,
                activity_type=LeadActivityType.NOTE,
                actor_id=actor_id,
                content=(
                    f"Marked as duplicate of lead {payload.duplicate_of_lead_id}. "
                    f"Reason: {payload.reason}"
                ),
                metadata={
                    "duplicate_of_lead_id": str(payload.duplicate_of_lead_id),
                    "reason": payload.reason,
                },
            )

        db.refresh(lead)
        return lead

    def assign_owner(
        self,
        db: Session,
        lead_id: UUID,
        business_id: UUID,
        actor_id: Optional[UUID],
        lead_owner_id: Optional[UUID],
    ) -> Lead:
        lead = self.get_lead(db, lead_id, business_id)

        with self._transaction(db):
            lead = self._leads.assign_owner(db, lead, lead_owner_id)
            self._record_activity(
                db, lead,
                activity_type=LeadActivityType.NOTE,
                actor_id=actor_id,
                content=(
                    f"Reassigned to {lead_owner_id}."
                    if lead_owner_id
                    else "Ownership cleared -- reverted to business account."
                ),
            )

        db.refresh(lead)
        return lead

    def soft_delete_lead(self, db: Session, lead_id: UUID, business_id: UUID) -> Lead:
        lead = self.get_lead(db, lead_id, business_id)
        with self._transaction(db):
            lead = self._leads.soft_delete(db, lead, datetime.now(timezone.utc))
        db.refresh(lead)
        return lead

    def restore_lead(self, db: Session, lead_id: UUID, business_id: UUID) -> Lead:
        lead = self._leads.get_by_id(db, lead_id, business_id, include_deleted=True)
        if lead is None:
            raise LeadNotFoundError(lead_id)
        with self._transaction(db):
            lead = self._leads.restore(db, lead)
        db.refresh(lead)
        return lead

    # ─────────────────────────────────────────────────────────────────
    # Activities
    # ─────────────────────────────────────────────────────────────────

    def log_activity(
        self,
        db: Session,
        lead_id: UUID,
        business_id: UUID,
        actor_id: Optional[UUID],
        payload: LeadActivityCreate,
    ) -> LeadActivity:
        lead = self.get_lead(db, lead_id, business_id)

        with self._transaction(db):
            activity = self._record_activity(
                db, lead,
                activity_type=payload.activity_type,
                actor_id=actor_id,
                content=payload.content,
                next_action_due=payload.next_action_due,
                # This endpoint is human-facing regardless of whether
                # actor_id happens to be populated; AI/system activities
                # are written internally by the agent layer, not through
                # this path.
                actor_type=LeadActivityActorType.HUMAN,
            )

            self._leads.touch_last_activity(db, lead, datetime.now(timezone.utc))
            if payload.activity_type == LeadActivityType.NOTE:
                self._leads.increment_notes_count(db, lead)

            # TODO(Stage 7): triggers lead_next_action_node and
            # lead_conversation_summarizer_node on `lead.activity_logged`.
            self._trigger_ai_enrichment(lead)

        db.refresh(activity)
        return activity

    def list_activities(
        self,
        db: Session,
        lead_id: UUID,
        business_id: UUID,
        **filters,
    ) -> Sequence[LeadActivity]:
        # Tenancy/existence check first, so a mismatched lead_id/
        # business_id fails clearly rather than silently returning [].
        self.get_lead(db, lead_id, business_id)
        return self._activities.list_by_lead(db, lead_id=lead_id, business_id=business_id, **filters)

    # ─────────────────────────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────────────────────────

    def _record_activity(
        self,
        db: Session,
        lead: Lead,
        activity_type: LeadActivityType,
        actor_id: Optional[UUID],
        content: str,
        metadata: Optional[dict] = None,
        next_action_due: Optional[datetime] = None,
        actor_type: Optional[LeadActivityActorType] = None,
    ) -> LeadActivity:
        """
        Shared LeadActivity write path -- every mutating method logs one.
        actor_type defaults to HUMAN when actor_id is present, else
        SYSTEM; callers with a fixed actor (initial creation is always
        SYSTEM-generated; log_activity() is always HUMAN-facing) pass
        actor_type explicitly to override the default.
        """
        activity = LeadActivity(
            lead_id=lead.id,
            business_id=lead.business_id,
            activity_type=activity_type,
            actor_type=actor_type or (
                LeadActivityActorType.HUMAN if actor_id else LeadActivityActorType.SYSTEM
            ),
            content=content,
            activity_metadata=metadata,
            next_action_due=next_action_due,
            created_by=actor_id,
        )
        return self._activities.create(db, activity)

    @staticmethod
    def _compute_lead_name(
        first_name: Optional[str],
        middle_name: Optional[str],
        last_name: Optional[str],
        company_name: Optional[str],
        email: Optional[str],
    ) -> str:
        """
        Cascade, mirroring ERPNext's set_full_name() + set_lead_name():
          1. full name from first/middle/last, if first_name present
          2. else company_name
          3. else local-part of email
          4. else -- unreachable in practice (LeadCreate's XOR validator
             already guarantees (1) or (2)); kept as a safety net
             matching ERPNext's own belt-and-suspenders throw.
        """
        if first_name:
            return " ".join(p for p in [first_name, middle_name, last_name] if p)
        if company_name:
            return company_name
        if email:
            return email.split("@")[0]
        raise LeadNameGenerationError(
            "Cannot compute lead_name: no first_name, company_name, or email available."
        )

    def _check_duplicate_lead(
        self, db: Session, business_id: UUID, payload: LeadCreate
    ) -> None:
        """
        PLACEHOLDER -- workflow step 2.

        TODO(Stage 7): real fuzzy duplicate detection (PAN/GSTIN/phone
        exact match OR company-name trigram similarity) is owned by
        lead_dedup_node, which runs asynchronously off the `lead.created`
        event and writes a *suggestion* to `duplicate_of_lead_id` for
        human review -- never a blocking throw, per the frozen
        validation rules. This method stays a no-op until then so Stage 7
        can slot the real check in without touching the surrounding
        workflow.
        """
        return None

    def _trigger_ai_enrichment(self, lead: Lead) -> None:
        """
        PLACEHOLDER -- workflow step 8.

        TODO(Stage 7): becomes the publish call into the `lead_events`
        Redis stream, consumed by lead_enricher_node, lead_scorer_node,
        lead_dedup_node, lead_next_action_node,
        lead_conversation_summarizer_node, and
        lead_business_size_estimator_node per the frozen AI spec. No
        event bus wiring, no LangGraph call here -- out of scope for the
        Service Layer stage.
        """
        return None

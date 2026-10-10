"""
Dependency providers for the CRM Lead API layer.

pure wiring -- constructs repositories/services and resolves auth context. No Business Logic , no SQL ,no ORM operations."
"""

from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.utils.auth_dependency import get_current_business_id

from app.crm.lead_domain.repositories.lead_activity_repository import LeadActivityRepository
from app.crm.lead_domain.repositories.lead_ai_insight_repository import LeadAIInsightRepository
from app.crm.lead_domain.repositories.lead_repository import LeadRepository
from app.crm.lead_domain.services.lead_service import LeadService


# LeadService holds no per-request state (only repository references), so
# a single module-level instance is reused across every request instead
# of re-constructing repositories on each call.

_lead_service = LeadService(
    lead_repository=LeadRepository(),
    activity_repository=LeadActivityRepository(),
    insight_repository=LeadAIInsightRepository(),
)

def get_lead_service() -> LeadService:
    """Provides the shared LeadService instance to route handlers."""
    return _lead_service

def get_current_business_uuid (
        business_id: str = Depends(get_current_business_id),
        )-> UUID:
    """
    Resolves the authenticated MSME's business_id as a UUID.

    Every CRM Lead endpoint scopes its query/mutation to this value --
    it is never accepted from the request body or path, per the
    cross-tenant isolation rule in the frozen spec.
    """
    return UUID(business_id)
def get_current_actor_id() -> Optional[UUID]:
    """
    Resolves the internal staff user performing this request, for
    created_by/updated_by/activity attribution.

    CreditBridge does not yet have staff-level (multi-user-per-business)
    authentication -- only the business-account JWT resolved by
    get_current_business_id. Per the frozen Lead spec, lead_owner_id and
    all actor-tracking fields are nullable-and-unenforced until that
    infra exists, so this resolves to None today.

    TODO: once staff/RBAC auth lands, replace this with a real dependency
    that decodes the staff user's identity from the request -- no
    changes required in LeadService or the router when that happens,
    since both already treat actor_id as Optional[UUID].
    """
    return None


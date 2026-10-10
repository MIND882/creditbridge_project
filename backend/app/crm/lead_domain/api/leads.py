"""
API Layer --- LEAD

SO YE FILE FRONTEND AND LEADSERVICE KE BEECH KA BRIDGE HAI 

IS ROUTER KA SIRF KAAAM  HAI :
- REQUEST RECEIVE KARNA
-  REQUIRED. DEPENDENCIES LIKE (DB, BUSINESS USER) LENA 
- LEAD SERVICE KO CALL KARNA
- RESPONSE RETURN KARNA
- SERVICE ERRORS KO PROPER HTTP STATUS LIKE (404,400,409, ETC.) ME CONVERT KARNA 

IS FILE ME :
- KOI BUSINESS LOGIC NAHI HOGI
- KOI SQL QUERY NAHI HOGI
- KOI ORM OPERATION NAHI HOGA

HAR CREATE, UPDATE, DELETE AUR READ OPERATION KA ACTUAL KAAM LEADSERVICE KAREGA. ROUTER SIRF HTTP LAYER HAI 

Stage 6 Final Changes:
1. Pehle har route me `except Exception` use ho raha tha.
   Ab sirf `LeadServiceError` catch hota hai.
   Isse agar coding bug aa jaye to wo hide nahi hoga,
   seedha 500 error ke saath traceback milega.

2. LeadStatus, LeadSource aur LeadQualificationStatus
   abhi models file se hi import kiye ja rahe hain.
   Isko future me `crm/enums.py` me move kiya ja sakta hai,
   lekin abhi Models freeze ho chuke hain,
   isliye Stage 6 me architecture ko touch nahi kiya gaya.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException,Query,status
from sqlalchemy.orm import Session

from app.db.session import get_db


from app.crm.lead_domain.api.deps import (
    get_current_business_id,
    get_current_business_uuid,
    get_current_actor_id,
    get_lead_service,
)
from app.crm.lead_domain.models.lead import LeadQualificationStatus, LeadSource, LeadStatus
from app.crm.lead_domain.schemas.lead import (
    LeadCreate,
    LeadListResponse,
    LeadListItem,
    LeadResponse,
    LeadUpdate,
)
from app.crm.lead_domain.services.lead_service import (
    InvalidStatusTransitionError,
    LeadNameGenerationError,
    LeadNotFoundError,
    LeadService,
    LeadServiceError,
)

router = APIRouter()

def _raise_for_service_error(exc: LeadServiceError)-> None:
    if isinstance(exc, LeadNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    elif isinstance(exc, InvalidStatusTransitionError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    elif isinstance(exc, LeadNameGenerationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    else:
        # Recognized as a domain error but not one of the specific cases
        # above -- still a known LeadServiceError, so 400 is appropriate
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
# ─────────────────────────────────────────────────────────────────────────────
# POST /v1/leads
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a Lead",
)
def create_lead(
    payload: LeadCreate,
    db: Session = Depends(get_db),
    business_id: UUID = Depends(get_current_business_uuid),
    actor_id: Optional[UUID] = Depends(get_current_actor_id),
    lead_service: LeadService = Depends(get_lead_service),
) -> LeadResponse:
    """
    Captures a new inquiry into the MSME's own sales pipeline.

    This is the entry point to the frozen Lead -> Opportunity ->
    Quotation -> Customer workflow -- every downstream stage traces back
    to a Lead created here.
    """
    try:
        lead = lead_service.create_lead(db, business_id, actor_id, payload)
    except LeadServiceError as exc:
        _raise_for_service_error(exc)
    return lead


# ─────────────────────────────────────────────────────────────────────────────
# GET /v1/leads
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=LeadListResponse,
    summary="List Leads",
)
def list_leads(
    status_filter: Optional[LeadStatus] = Query(None, alias="status"),
    qualification_status: Optional[LeadQualificationStatus] = Query(None),
    source: Optional[LeadSource] = Query(None),
    lead_owner_id: Optional[UUID] = Query(None),
    ca_partner_id: Optional[UUID] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    business_id: UUID = Depends(get_current_business_uuid),
    lead_service: LeadService = Depends(get_lead_service),
) -> LeadListResponse:
    """
    Paginated, filterable pipeline view -- the primary listing surface
    sales reps and admins use to work their Lead queue day to day.

    Filters mirror the composite/partial indexes frozen in the Stage 2
    migration (business+status, business+qualification, etc.), so this
    endpoint's query shapes are index-backed by design, not by accident.
    """
    offset = (page - 1) * page_size
    items, total = lead_service.list_leads(
        db,
        business_id=business_id,
        status=status_filter,
        qualification_status=qualification_status,
        source=source,
        lead_owner_id=lead_owner_id,
        ca_partner_id=ca_partner_id,
        offset=offset,
        limit=page_size,
    )
    return LeadListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[LeadListItem.model_validate(lead) for lead in items],
    )


# ─────────────────────────────────────────────────────────────────────────────
# GET /v1/leads/{lead_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
    summary="Get Lead detail",
)
def get_lead(
    lead_id: UUID,
    db: Session = Depends(get_db),
    business_id: UUID = Depends(get_current_business_uuid),
    lead_service: LeadService = Depends(get_lead_service),
) -> LeadResponse:
    """
    Full-detail view for a single Lead, including the AI cache fields
    (ai_lead_score, kyc_precheck) that the list endpoint deliberately
    omits to keep pagination responses lightweight.
    """
    try:
        lead = lead_service.get_lead(db, lead_id, business_id)
    except LeadServiceError as exc:
        _raise_for_service_error(exc)
    return lead


# ─────────────────────────────────────────────────────────────────────────────
# PUT /v1/leads/{lead_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.put(
    "/{lead_id}",
    response_model=LeadResponse,
    summary="Update a Lead",
)
def update_lead(
    lead_id: UUID,
    payload: LeadUpdate,
    db: Session = Depends(get_db),
    business_id: UUID = Depends(get_current_business_uuid),
    actor_id: Optional[UUID] = Depends(get_current_actor_id),
    lead_service: LeadService = Depends(get_lead_service),
) -> LeadResponse:
    """
    Edits a Lead's own fields (contact details, org info, source
    attribution, etc.).

    Deliberately cannot change status, ai_lead_score, kyc_precheck,
    duplicate_of_lead_id, or converted_opportunity_id -- those are owned
    by dedicated workflow endpoints (qualify / mark-duplicate / convert)
    and internal services, per the frozen status-transition rules. This
    is enforced by LeadUpdate's schema shape (Stage 3), not by this
    router.
    """
    try:
        lead = lead_service.update_lead(db, lead_id, business_id, actor_id, payload)
    except LeadServiceError as exc:
        _raise_for_service_error(exc)
    return lead


# ─────────────────────────────────────────────────────────────────────────────
# DELETE /v1/leads/{lead_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.delete(
    "/{lead_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete a Lead",
)
def delete_lead(
    lead_id: UUID,
    db: Session = Depends(get_db),
    business_id: UUID = Depends(get_current_business_uuid),
    lead_service: LeadService = Depends(get_lead_service),
) -> None:
    """
    Soft-deletes a Lead (is_deleted=True), matching ERPNext's
    cascading-cleanup intent without a hard DELETE -- the row and its
    activity/attachment/AI-insight history remain recoverable via the
    (currently service-only) restore path.

    204 with no body: the caller asked to remove the resource from their
    view; there's nothing meaningful left to return.
    """
    try:
        lead_service.soft_delete_lead(db, lead_id, business_id)
    except LeadServiceError as exc:
        _raise_for_service_error(exc)
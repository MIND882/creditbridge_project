"""
Opportunity API routes.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.crm.opportunity_domain.models.opportunity import OpportunityStatus
from app.crm.opportunity_domain.repositories.opportunity_repository import OpportunityRepository
from app.crm.opportunity_domain.schemas.opportunity import (
    OpportunityConvertToCustomerPayload,
    OpportunityCreatePayload,
    OpportunityListResponse,
    OpportunityMarkLostPayload,
    OpportunityResponse,
    OpportunityUpdatePayload,
)
from app.crm.opportunity_domain.services.opportunity_service import OpportunityService
from app.crm.lead_domain.repositories.lead_repository import LeadRepository
from app.customers.repositories.customer_repository import CustomerRepository
from app.customers.schemas.customer import CustomerResponse
from app.customers.services.customer_service import CustomerService
from app.db.session import get_db
from app.crm.lead_domain.api.deps import get_current_business_uuid

# We assume get_current_user_id exists in auth_dependency, but in deps.py
# it currently returns None for the single-MSME reality.
from app.crm.lead_domain.api.deps import get_current_actor_id as get_current_user_id

router = APIRouter(tags=["opportunities"])


def get_opportunity_service(db: Session = Depends(get_db)) -> OpportunityService:
    customer_service = CustomerService(CustomerRepository(db))
    lead_repository = LeadRepository() # Based on deps.py pattern
    return OpportunityService(
        db, OpportunityRepository(db), customer_service, lead_repository
    )


@router.post("", response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_opportunity(
    payload: OpportunityCreatePayload,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    user_id: Optional[uuid.UUID] = Depends(get_current_user_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.create_opportunity(payload, business_id, created_by=user_id)


@router.get("", response_model=OpportunityListResponse)
def list_opportunities(
    status_filter: Optional[OpportunityStatus] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: OpportunityService = Depends(get_opportunity_service),
):
    items, total = service.list_opportunities(
        business_id, status_filter=status_filter, page=page, page_size=page_size
    )
    return OpportunityListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(
    opportunity_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.get_opportunity(opportunity_id, business_id)


@router.patch("/{opportunity_id}", response_model=OpportunityResponse)
def update_opportunity(
    opportunity_id: uuid.UUID,
    payload: OpportunityUpdatePayload,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    user_id: Optional[uuid.UUID] = Depends(get_current_user_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.update_opportunity(opportunity_id, business_id, payload, updated_by=user_id)


@router.post("/{opportunity_id}/mark-lost", response_model=OpportunityResponse)
def mark_opportunity_lost(
    opportunity_id: uuid.UUID,
    payload: OpportunityMarkLostPayload,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    user_id: Optional[uuid.UUID] = Depends(get_current_user_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.mark_lost(opportunity_id, business_id, payload, updated_by=user_id)


@router.post("/{opportunity_id}/reopen", response_model=OpportunityResponse)
def reopen_opportunity(
    opportunity_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.reopen(opportunity_id, business_id)


@router.post(
    "/{opportunity_id}/convert-to-customer",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def convert_opportunity_to_customer(
    opportunity_id: uuid.UUID,
    payload: OpportunityConvertToCustomerPayload,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    user_id: Optional[uuid.UUID] = Depends(get_current_user_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    """Implements the whiteboard's "Skip Quotation, Convert to Customer" path."""
    return service.convert_to_customer(
        opportunity_id,
        business_id,
        company_name=payload.company_name,
        contact_name=payload.contact_name,
        contact_email=payload.contact_email,
        contact_phone=payload.contact_phone,
        created_by=user_id,
    )


@router.delete("/{opportunity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_opportunity(
    opportunity_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: OpportunityService = Depends(get_opportunity_service),
):
    service.delete_opportunity(opportunity_id, business_id)

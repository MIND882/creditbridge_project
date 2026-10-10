# app/crm/quotation_domain/api/quotation.py

"""
Quotation API routes.

ASSUMPTION: matches the import/dependency style confirmed working for
Opportunity's API file — verify these paths are still correct:
  - backend.app.crm.lead_domain.api.deps.get_current_business_uuid
  - backend.app.crm.lead_domain.api.deps.get_current_actor_id
  - backend.app.db.session.get_db
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.crm.lead_domain.api.deps import get_current_business_uuid
from backend.app.crm.lead_domain.api.deps import get_current_actor_id as get_current_user_id
from backend.app.crm.opportunity_domain.repositories.opportunity_repository import (
    OpportunityRepository,
)
from backend.app.crm.quotation_domain.models.quotation import QuotationStatus
from backend.app.crm.quotation_domain.repositories.quotation_repository import (
    QuotationRepository,
)
from backend.app.crm.quotation_domain.schemas.quotation import (
    QuotationAcceptPayload,
    QuotationCreatePayload,
    QuotationListResponse,
    QuotationRejectPayload,
    QuotationResponse,
    QuotationUpdatePayload,
)
from backend.app.crm.quotation_domain.services.quotation_service import QuotationService
from backend.app.customers.repositories.customer_repository import CustomerRepository
from backend.app.customers.schemas.customer import CustomerResponse
from backend.app.customers.services.customer_service import CustomerService
from backend.app.db.session import get_db

router = APIRouter(tags=["quotations"])  # prefix assigned in main.py, per established convention


def get_quotation_service(db: Session = Depends(get_db)) -> QuotationService:
    customer_service = CustomerService(CustomerRepository(db))
    opportunity_repository = OpportunityRepository(db)
    return QuotationService(QuotationRepository(db), opportunity_repository, customer_service)


@router.post("", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
def create_quotation(
    payload: QuotationCreatePayload,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    user_id: Optional[uuid.UUID] = Depends(get_current_user_id),
    service: QuotationService = Depends(get_quotation_service),
):
    return service.create_quotation(payload, business_id, created_by=user_id)


@router.get("", response_model=QuotationListResponse)
def list_quotations(
    status_filter: Optional[QuotationStatus] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: QuotationService = Depends(get_quotation_service),
):
    items, total = service.list_quotations(
        business_id, status_filter=status_filter, page=page, page_size=page_size
    )
    return QuotationListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{quotation_id}", response_model=QuotationResponse)
def get_quotation(
    quotation_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: QuotationService = Depends(get_quotation_service),
):
    return service.get_quotation(quotation_id, business_id)


@router.patch("/{quotation_id}", response_model=QuotationResponse)
def update_quotation(
    quotation_id: uuid.UUID,
    payload: QuotationUpdatePayload,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    user_id: Optional[uuid.UUID] = Depends(get_current_user_id),
    service: QuotationService = Depends(get_quotation_service),
):
    return service.update_quotation(quotation_id, business_id, payload, updated_by=user_id)


@router.post("/{quotation_id}/send", response_model=QuotationResponse)
def send_quotation(
    quotation_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    user_id: Optional[uuid.UUID] = Depends(get_current_user_id),
    service: QuotationService = Depends(get_quotation_service),
):
    return service.send(quotation_id, business_id, updated_by=user_id)


@router.post("/{quotation_id}/reject", response_model=QuotationResponse)
def reject_quotation(
    quotation_id: uuid.UUID,
    payload: QuotationRejectPayload,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    user_id: Optional[uuid.UUID] = Depends(get_current_user_id),
    service: QuotationService = Depends(get_quotation_service),
):
    return service.reject(quotation_id, business_id, payload, updated_by=user_id)


@router.post(
    "/{quotation_id}/accept",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def accept_quotation(
    quotation_id: uuid.UUID,
    payload: QuotationAcceptPayload,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    user_id: Optional[uuid.UUID] = Depends(get_current_user_id),
    service: QuotationService = Depends(get_quotation_service),
):
    """Terminal conversion point: Lead -> Opportunity -> Quotation -> Customer."""
    return service.accept(quotation_id, business_id, payload, created_by=user_id)


@router.delete("/{quotation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quotation(
    quotation_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: QuotationService = Depends(get_quotation_service),
):
    service.delete_quotation(quotation_id, business_id)
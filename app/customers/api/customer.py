"""
Customer API routes.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.customers.models.customer import CustomerStatus
from app.customers.repositories.customer_repository import CustomerRepository
from app.customers.schemas.customer import (
    CustomerCreatePayload,
    CustomerListResponse,
    CustomerResponse,
    CustomerUpdatePayload,
)
from app.customers.services.customer_service import CustomerService
from app.db.session import get_db
from app.utils.auth_dependency import get_current_business_id

router = APIRouter(tags=["customers"])


def get_current_business_uuid(business_id: str = Depends(get_current_business_id)) -> uuid.UUID:
    return uuid.UUID(business_id)


def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(CustomerRepository(db))


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: CustomerCreatePayload,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: CustomerService = Depends(get_customer_service),
):
    # created_by is set to None for now as per CreditBridge single-owner reality
    return service.create_customer(payload, business_id, created_by=None)


@router.get("", response_model=CustomerListResponse)
def list_customers(
    status_filter: Optional[CustomerStatus] = Query(None, alias="status"),
    search: Optional[str] = Query(None, max_length=255),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: CustomerService = Depends(get_customer_service),
):
    items, total = service.list_customers(
        business_id,
        status_filter=status_filter,
        search=search,
        page=page,
        page_size=page_size,
    )
    return CustomerListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: CustomerService = Depends(get_customer_service),
):
    return service.get_customer(customer_id, business_id)


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: uuid.UUID,
    payload: CustomerUpdatePayload,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: CustomerService = Depends(get_customer_service),
):
    return service.update_customer(customer_id, business_id, payload, updated_by=None)


@router.post("/{customer_id}/deactivate", response_model=CustomerResponse)
def deactivate_customer(
    customer_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: CustomerService = Depends(get_customer_service),
):
    return service.deactivate_customer(customer_id, business_id)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    service: CustomerService = Depends(get_customer_service),
):
    service.delete_customer(customer_id, business_id)

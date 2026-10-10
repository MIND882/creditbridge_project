"""
Business logic for the Customer domain.
"""

import uuid
from typing import Optional

from fastapi import HTTPException, status

from app.customers.models.customer import Customer, CustomerStatus
from app.customers.repositories.customer_repository import CustomerRepository
from app.customers.schemas.customer import (
    CustomerCreatePayload,
    CustomerIntelligenceUpdatePayload,
    CustomerUpdatePayload,
)


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def create_customer(
        self, payload: CustomerCreatePayload, business_id: uuid.UUID, created_by: Optional[uuid.UUID]
    ) -> Customer:
        if payload.gstin and self.repository.exists_with_gstin(payload.gstin, business_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A customer with GSTIN {payload.gstin} already exists for this business.",
            )

        customer = Customer(
            business_id=business_id,
            customer_name=payload.customer_name,
            customer_group=payload.customer_group,
            territory=payload.territory,
            industry=payload.industry,
            primary_contact_name=payload.primary_contact_name,
            primary_contact_email=payload.primary_contact_email,
            primary_contact_phone=payload.primary_contact_phone,
            address_line=payload.address_line,
            city=payload.city,
            state=payload.state,
            country=payload.country,
            pincode=payload.pincode,
            gstin=payload.gstin,
            pan=payload.pan,
            converted_from_lead_id=payload.converted_from_lead_id,
            converted_from_opportunity_id=payload.converted_from_opportunity_id,
            converted_from_quotation_id=payload.converted_from_quotation_id,
            status=CustomerStatus.ACTIVE,
            created_by=created_by,
        )
        return self.repository.create(customer)

    def get_customer(self, customer_id: uuid.UUID, business_id: uuid.UUID) -> Customer:
        customer = self.repository.get_by_id(customer_id, business_id)
        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found."
            )
        return customer

    def list_customers(
        self,
        business_id: uuid.UUID,
        *,
        status_filter: Optional[CustomerStatus] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[list[Customer], int]:
        return self.repository.list_by_business(
            business_id, status=status_filter, search=search, page=page, page_size=page_size
        )

    def update_customer(
        self,
        customer_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: CustomerUpdatePayload,
        updated_by: Optional[uuid.UUID],
    ) -> Customer:
        customer = self.get_customer(customer_id, business_id)

        if payload.gstin and payload.gstin != customer.gstin:
            if self.repository.exists_with_gstin(
                payload.gstin, business_id, exclude_id=customer_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"A customer with GSTIN {payload.gstin} already exists for this business.",
                )

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        customer.updated_by = updated_by

        return self.repository.update(customer)

    def update_intelligence_fields(
        self,
        customer_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: CustomerIntelligenceUpdatePayload,
    ) -> Customer:
        customer = self.get_customer(customer_id, business_id)
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        return self.repository.update(customer)

    def deactivate_customer(self, customer_id: uuid.UUID, business_id: uuid.UUID) -> Customer:
        customer = self.get_customer(customer_id, business_id)
        customer.status = CustomerStatus.INACTIVE
        return self.repository.update(customer)

    def delete_customer(self, customer_id: uuid.UUID, business_id: uuid.UUID) -> None:
        customer = self.get_customer(customer_id, business_id)
        self.repository.soft_delete(customer)

    def get_or_create_from_lead(
        self,
        *,
        business_id: uuid.UUID,
        lead_id: uuid.UUID,
        lead_company_name: str,
        lead_contact_name: Optional[str],
        lead_email: Optional[str],
        lead_phone: Optional[str],
        lead_city: Optional[str],
        lead_state: Optional[str],
        lead_gstin: Optional[str],
        created_by: Optional[uuid.UUID],
    ) -> Customer:
        existing = self.repository.get_by_lead_id(lead_id, business_id)
        if existing is not None:
            return existing

        payload = CustomerCreatePayload(
            customer_name=lead_company_name,
            primary_contact_name=lead_contact_name,
            primary_contact_email=lead_email,
            primary_contact_phone=lead_phone,
            city=lead_city,
            state=lead_state,
            country="India",
            gstin=lead_gstin,
            converted_from_lead_id=lead_id,
        )
        return self.create_customer(payload, business_id, created_by)

    def get_or_create_from_opportunity(
        self,
        *,
        business_id: uuid.UUID,
        opportunity_id: uuid.UUID,
        lead_id: Optional[uuid.UUID],
        company_name: str,
        contact_name: Optional[str],
        contact_email: Optional[str],
        contact_phone: Optional[str],
        created_by: Optional[uuid.UUID],
    ) -> Customer:
        if lead_id is not None:
            existing = self.repository.get_by_lead_id(lead_id, business_id)
            if existing is not None:
                existing.converted_from_opportunity_id = opportunity_id
                return self.repository.update(existing)

        payload = CustomerCreatePayload(
            customer_name=company_name,
            primary_contact_name=contact_name,
            primary_contact_email=contact_email,
            primary_contact_phone=contact_phone,
            country="India",
            converted_from_lead_id=lead_id,
            converted_from_opportunity_id=opportunity_id,
        )
        return self.create_customer(payload, business_id, created_by)

    def get_or_create_from_quotation(
        self,
        *,
        business_id: uuid.UUID,
        quotation_id: uuid.UUID,
        opportunity_id: Optional[uuid.UUID],
        lead_id: Optional[uuid.UUID],
        company_name: str,
        contact_name: Optional[str],
        contact_email: Optional[str],
        contact_phone: Optional[str],
        created_by: Optional[uuid.UUID],
    ) -> Customer:
        if lead_id is not None:
            existing = self.repository.get_by_lead_id(lead_id, business_id)
            if existing is not None:
                existing.converted_from_opportunity_id = (
                    opportunity_id or existing.converted_from_opportunity_id
                )
                existing.converted_from_quotation_id = quotation_id
                return self.repository.update(existing)

        payload = CustomerCreatePayload(
            customer_name=company_name,
            primary_contact_name=contact_name,
            primary_contact_email=contact_email,
            primary_contact_phone=contact_phone,
            country="India",
            converted_from_lead_id=lead_id,
            converted_from_opportunity_id=opportunity_id,
            converted_from_quotation_id=quotation_id,
        )
        return self.create_customer(payload, business_id, created_by)

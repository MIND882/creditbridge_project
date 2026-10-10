"""
Business logic for the Opportunity domain.

Dependency direction: this service MAY import from `app.customers`
(Customer is a core entity that CRM depends on) and from other `app.crm`
submodules (e.g. Lead repository). It must NEVER be imported BY
`app.customers` — that would invert the dependency direction.
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crm.opportunity_domain.models.opportunity import Opportunity, OpportunityStatus
from app.crm.opportunity_domain.repositories.opportunity_repository import OpportunityRepository
from app.crm.opportunity_domain.schemas.opportunity import (
    OpportunityCreatePayload,
    OpportunityMarkLostPayload,
    OpportunityUpdatePayload,
)
from app.customers.models.customer import Customer
from app.customers.services.customer_service import CustomerService
from app.crm.lead_domain.repositories.lead_repository import LeadRepository


class OpportunityService:
    def __init__(
        self,
        db: Session,
        repository: OpportunityRepository,
        customer_service: CustomerService,
        lead_repository: LeadRepository,
    ):
        self.db = db
        self.repository = repository
        self.customer_service = customer_service
        self.lead_repository = lead_repository

    # ── Standard CRUD ────────────────────────────────────────────────────

    def create_opportunity(
        self,
        payload: OpportunityCreatePayload,
        business_id: uuid.UUID,
        created_by: uuid.UUID,
    ) -> Opportunity:
        # Validate the referenced party actually exists in this tenant
        # before insert — gives a clean 404 instead of a raw FK violation.
        if payload.lead_id is not None:
            lead = self.lead_repository.get_by_id(self.db, payload.lead_id, business_id)
            if lead is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Referenced lead not found.",
                )
        if payload.customer_id is not None:
            self.customer_service.get_customer(payload.customer_id, business_id)
            # raises 404 internally if not found

        opportunity = Opportunity(
            business_id=business_id,
            lead_id=payload.lead_id,
            customer_id=payload.customer_id,
            title=payload.title,
            opportunity_amount=payload.opportunity_amount,
            currency=payload.currency,
            status=OpportunityStatus.OPEN,
            sales_stage=payload.sales_stage,
            probability=payload.probability,
            expected_closing_date=payload.expected_closing_date,
            opportunity_owner_id=payload.opportunity_owner_id,
            created_by=created_by,
        )
        return self.repository.create(opportunity)

    def get_opportunity(
        self, opportunity_id: uuid.UUID, business_id: uuid.UUID
    ) -> Opportunity:
        opportunity = self.repository.get_by_id(opportunity_id, business_id)
        if opportunity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found."
            )
        return opportunity

    def list_opportunities(
        self,
        business_id: uuid.UUID,
        *,
        status_filter: Optional[OpportunityStatus] = None,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[list[Opportunity], int]:
        return self.repository.list_by_business(
            business_id, status=status_filter, page=page, page_size=page_size
        )

    def update_opportunity(
        self,
        opportunity_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: OpportunityUpdatePayload,
        updated_by: uuid.UUID,
    ) -> Opportunity:
        opportunity = self.get_opportunity(opportunity_id, business_id)

        if opportunity.status == OpportunityStatus.LOST:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot update a Lost opportunity. Reopen it first if needed.",
            )

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(opportunity, field, value)
        opportunity.updated_by = updated_by

        return self.repository.update(opportunity)

    def delete_opportunity(self, opportunity_id: uuid.UUID, business_id: uuid.UUID) -> None:
        opportunity = self.get_opportunity(opportunity_id, business_id)
        self.repository.soft_delete(opportunity)

    # ── Lost tracking ─────────────────────────────────────────────────────

    def mark_lost(
        self,
        opportunity_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: OpportunityMarkLostPayload,
        updated_by: uuid.UUID,
    ) -> Opportunity:
        opportunity = self.get_opportunity(opportunity_id, business_id)

        # TODO(quotation-dependency): block this if an active Quotation
        # exists for this opportunity, once app.crm.quotation exists.

        opportunity.status = OpportunityStatus.LOST
        opportunity.lost_reason = payload.lost_reason
        opportunity.competitor = payload.competitor
        opportunity.updated_by = updated_by

        return self.repository.update(opportunity)

    def reopen(self, opportunity_id: uuid.UUID, business_id: uuid.UUID) -> Opportunity:
        opportunity = self.get_opportunity(opportunity_id, business_id)
        opportunity.status = OpportunityStatus.OPEN
        opportunity.lost_reason = None
        opportunity.competitor = None
        return self.repository.update(opportunity)

    # ── Auto-close scheduled job ────────────────────────────────────────

    def auto_close_stale_opportunities(
        self, business_id: uuid.UUID, stale_after_days: int = 15
    ) -> int:
        stale_since = datetime.now(timezone.utc) - timedelta(days=stale_after_days)
        stale_opportunities = self.repository.list_open_stale(business_id, stale_since)
        for opp in stale_opportunities:
            opp.status = OpportunityStatus.CLOSED
            self.repository.update(opp)
        return len(stale_opportunities)

    # ── Conversion to Customer ──────────────────────────────────────────

    def convert_to_customer(
        self,
        opportunity_id: uuid.UUID,
        business_id: uuid.UUID,
        *,
        company_name: str,
        contact_name: Optional[str],
        contact_email: Optional[str],
        contact_phone: Optional[str],
        created_by: uuid.UUID,
    ) -> Customer:
        opportunity = self.get_opportunity(opportunity_id, business_id)

        if opportunity.customer_id is not None:
            # This Opportunity originated FROM an existing Customer already
            # — nothing to convert, it's already tied to a Customer.
            return self.customer_service.get_customer(opportunity.customer_id, business_id)

        if opportunity.converted_customer_id is not None:
            # Already converted previously — idempotent return.
            return self.customer_service.get_customer(
                opportunity.converted_customer_id, business_id
            )

        customer = self.customer_service.get_or_create_from_opportunity(
            business_id=business_id,
            opportunity_id=opportunity.id,
            lead_id=opportunity.lead_id,
            company_name=company_name,
            contact_name=contact_name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            created_by=created_by,
        )

        opportunity.status = OpportunityStatus.WON
        # Set converted_customer_id (outcome), NOT customer_id (origin)
        opportunity.converted_customer_id = customer.id
        self.repository.update(opportunity)

        return customer

# app/crm/quotation_domain/services/quotation_service.py

"""
Business logic for the Quotation domain.

Dependency direction: this service depends on `app.customers` (to create/
reuse a Customer on Accept) and on the Opportunity repository (to update
the linked Opportunity's status/converted_customer_id). It must never be
imported BY those modules — same rule as OpportunityService.
"""

import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException, status

from app.crm.opportunity_domain.models.opportunity import OpportunityStatus
from app.crm.opportunity_domain.repositories.opportunity_repository import OpportunityRepository
from app.crm.quotation_domain.models.quotation import (
    Quotation,
    QuotationItem,
    QuotationPaymentScheduleEntry,
    QuotationStatus,
    QuotationTax,
)
from app.crm.quotation_domain.repositories.quotation_repository import QuotationRepository
from app.crm.quotation_domain.schemas.quotation import (
    QuotationAcceptPayload,
    QuotationCreatePayload,
    QuotationItemPayload,
    QuotationPaymentScheduleEntryPayload,
    QuotationRejectPayload,
    QuotationTaxPayload,
    QuotationUpdatePayload,
)
from app.customers.models.customer import Customer
from app.customers.services.customer_service import CustomerService


class QuotationService:
    def __init__(
        self,
        repository: QuotationRepository,
        opportunity_repository: OpportunityRepository,
        customer_service: CustomerService,
    ):
        self.repository = repository
        self.opportunity_repository = opportunity_repository
        self.customer_service = customer_service

    # ── Totals calculation ───────────────────────────────────────────────
    # Mirrors ERPNext's calculate_taxes_and_totals — simplified since we
    # don't have a Pricing Rule evaluation engine or a GST tax-computation
    # engine (that's Phase 3). This computes item-line totals and applies
    # whatever tax lines / discounts were explicitly passed in, rather
    # than deriving tax amounts from a rule engine.

    @staticmethod
    def _calculate_totals(quotation: Quotation) -> None:
        total_qty = Decimal(0)
        net_total = Decimal(0)

        for item in quotation.items:
            item.amount = (item.qty or Decimal(0)) * (item.rate or Decimal(0))
            total_qty += item.qty or Decimal(0)
            net_total += item.amount

        total_taxes = Decimal(0)
        for tax in quotation.taxes:
            tax.total = net_total + total_taxes + tax.tax_amount
            total_taxes += tax.tax_amount

        quotation.total_qty = total_qty
        quotation.total = net_total
        quotation.net_total = net_total
        quotation.base_total = net_total * (quotation.conversion_rate or Decimal(1))
        quotation.base_net_total = quotation.base_total
        quotation.total_taxes_and_charges = total_taxes
        quotation.base_total_taxes_and_charges = total_taxes * (
            quotation.conversion_rate or Decimal(1)
        )

        discount = quotation.discount_amount or Decimal(0)
        grand_total = net_total + total_taxes - discount
        quotation.grand_total = grand_total
        quotation.rounded_total = grand_total.quantize(Decimal("1"))
        quotation.rounding_adjustment = quotation.rounded_total - grand_total
        quotation.base_grand_total = grand_total * (quotation.conversion_rate or Decimal(1))
        quotation.base_rounded_total = quotation.rounded_total * (
            quotation.conversion_rate or Decimal(1)
        )

    @staticmethod
    def _build_items(payloads: list[QuotationItemPayload]) -> list[QuotationItem]:
        return [
            QuotationItem(
                item_name=p.item_name,
                description=p.description,
                qty=p.qty,
                uom=p.uom,
                rate=p.rate,
                amount=p.qty * p.rate,
                is_alternative=p.is_alternative,
                is_free_item=p.is_free_item,
            )
            for p in payloads
        ]

    @staticmethod
    def _build_taxes(payloads: list[QuotationTaxPayload]) -> list[QuotationTax]:
        return [
            QuotationTax(
                charge_type=p.charge_type,
                description=p.description,
                rate=p.rate,
                tax_amount=p.tax_amount,
                total=p.tax_amount,
            )
            for p in payloads
        ]

    @staticmethod
    def _build_payment_schedule(
        payloads: list[QuotationPaymentScheduleEntryPayload],
    ) -> list[QuotationPaymentScheduleEntry]:
        return [
            QuotationPaymentScheduleEntry(
                description=p.description,
                due_date=p.due_date,
                invoice_portion_percent=p.invoice_portion_percent,
                payment_amount=p.payment_amount,
            )
            for p in payloads
        ]

    # ── Standard CRUD ────────────────────────────────────────────────────

    def create_quotation(
        self,
        payload: QuotationCreatePayload,
        business_id: uuid.UUID,
        created_by: uuid.UUID,
    ) -> Quotation:
        opportunity = self.opportunity_repository.get_by_id(payload.opportunity_id, business_id)
        if opportunity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Referenced opportunity not found."
            )

        quotation = Quotation(
            business_id=business_id,
            opportunity_id=payload.opportunity_id,
            title=payload.title,
            transaction_date=payload.transaction_date or date.today(),
            valid_till=payload.valid_till,
            order_type=payload.order_type,
            has_unit_price_items=payload.has_unit_price_items,
            currency=payload.currency,
            conversion_rate=payload.conversion_rate,
            selling_price_list=payload.selling_price_list,
            price_list_currency=payload.price_list_currency,
            plc_conversion_rate=payload.plc_conversion_rate,
            ignore_pricing_rule=payload.ignore_pricing_rule,
            pricing_rules=payload.pricing_rules,
            tax_category=payload.tax_category,
            taxes_and_charges_template=payload.taxes_and_charges_template,
            shipping_rule=payload.shipping_rule,
            incoterm=payload.incoterm,
            named_place=payload.named_place,
            apply_discount_on=payload.apply_discount_on,
            additional_discount_percentage=payload.additional_discount_percentage,
            discount_amount=payload.discount_amount,
            coupon_code=payload.coupon_code,
            referral_sales_partner=payload.referral_sales_partner,
            payment_terms_template=payload.payment_terms_template,
            payment_due_date=payload.payment_due_date,
            payment_amount=payload.payment_amount,
            tc_name=payload.tc_name,
            terms=payload.terms,
            letter_head=payload.letter_head,
            group_same_items=payload.group_same_items,
            select_print_heading=payload.select_print_heading,
            language=payload.language,
            customer_address=payload.customer_address,
            shipping_address=payload.shipping_address,
            company_address=payload.company_address,
            contact_person=payload.contact_person,
            contact_mobile=payload.contact_mobile,
            contact_email=payload.contact_email,
            utm_source=payload.utm_source,
            utm_medium=payload.utm_medium,
            utm_campaign=payload.utm_campaign,
            utm_content=payload.utm_content,
            scan_barcode=payload.scan_barcode,
            customer_group=payload.customer_group,
            territory=payload.territory,
            status=QuotationStatus.DRAFT,
            items=self._build_items(payload.items),
            taxes=self._build_taxes(payload.taxes),
            payment_schedule_entries=self._build_payment_schedule(payload.payment_schedule_entries),
            created_by=created_by,
        )
        self._calculate_totals(quotation)
        return self.repository.create(quotation)

    def get_quotation(self, quotation_id: uuid.UUID, business_id: uuid.UUID) -> Quotation:
        quotation = self.repository.get_by_id(quotation_id, business_id)
        if quotation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found."
            )
        return quotation

    def list_quotations(
        self,
        business_id: uuid.UUID,
        *,
        status_filter: Optional[QuotationStatus] = None,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[list[Quotation], int]:
        return self.repository.list_by_business(
            business_id, status=status_filter, page=page, page_size=page_size
        )

    def update_quotation(
        self,
        quotation_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: QuotationUpdatePayload,
        updated_by: uuid.UUID,
    ) -> Quotation:
        quotation = self.get_quotation(quotation_id, business_id)

        if quotation.status in (QuotationStatus.ACCEPTED, QuotationStatus.REJECTED, QuotationStatus.CANCELLED):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot update a quotation in '{quotation.status.value}' status.",
            )

        update_data = payload.model_dump(exclude_unset=True, exclude={"items", "taxes", "payment_schedule_entries"})
        for field, value in update_data.items():
            setattr(quotation, field, value)

        if payload.items is not None:
            self.repository.replace_items(quotation, self._build_items(payload.items))
        if payload.taxes is not None:
            self.repository.replace_taxes(quotation, self._build_taxes(payload.taxes))
        if payload.payment_schedule_entries is not None:
            self.repository.replace_payment_schedule(
                quotation, self._build_payment_schedule(payload.payment_schedule_entries)
            )

        quotation.updated_by = updated_by
        self._calculate_totals(quotation)
        return self.repository.update(quotation)

    def delete_quotation(self, quotation_id: uuid.UUID, business_id: uuid.UUID) -> None:
        quotation = self.get_quotation(quotation_id, business_id)
        self.repository.soft_delete(quotation)

    # ── Status transitions ───────────────────────────────────────────────

    def send(self, quotation_id: uuid.UUID, business_id: uuid.UUID, updated_by: uuid.UUID) -> Quotation:
        quotation = self.get_quotation(quotation_id, business_id)
        if quotation.status != QuotationStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Only a Draft quotation can be sent.",
            )
        quotation.status = QuotationStatus.SENT
        quotation.updated_by = updated_by
        self.repository.update(quotation)

        # Mirrors ERPNext's on_submit -> update_opportunity("Quotation")
        opportunity = self.opportunity_repository.get_by_id(quotation.opportunity_id, business_id)
        if opportunity is not None and opportunity.status == OpportunityStatus.OPEN:
            opportunity.status = OpportunityStatus.QUOTATION_SENT
            self.opportunity_repository.update(opportunity)

        return quotation

    def reject(
        self,
        quotation_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: QuotationRejectPayload,
        updated_by: uuid.UUID,
    ) -> Quotation:
        quotation = self.get_quotation(quotation_id, business_id)
        if quotation.status not in (QuotationStatus.SENT, QuotationStatus.PARTIALLY_ORDERED):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Only a Sent quotation can be rejected.",
            )
        quotation.status = QuotationStatus.REJECTED
        quotation.rejection_reason = payload.rejection_reason
        quotation.lost_reasons = payload.lost_reasons
        quotation.competitors = payload.competitors
        quotation.updated_by = updated_by
        return self.repository.update(quotation)

    def accept(
        self,
        quotation_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: QuotationAcceptPayload,
        created_by: uuid.UUID,
    ) -> Customer:
        """
        Terminal conversion point of the full funnel:
        Lead -> Opportunity -> Quotation -> Accept -> Customer.
        """
        quotation = self.get_quotation(quotation_id, business_id)
        if quotation.status != QuotationStatus.SENT:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Only a Sent quotation can be accepted.",
            )

        opportunity = self.opportunity_repository.get_by_id(quotation.opportunity_id, business_id)
        if opportunity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Linked opportunity not found."
            )

        customer = self.customer_service.get_or_create_from_quotation(
            business_id=business_id,
            quotation_id=quotation.id,
            opportunity_id=opportunity.id,
            lead_id=opportunity.lead_id,
            company_name=payload.company_name,
            contact_name=payload.contact_name,
            contact_email=payload.contact_email,
            contact_phone=payload.contact_phone,
            created_by=created_by,
        )

        quotation.status = QuotationStatus.ACCEPTED
        quotation.converted_customer_id = customer.id
        self.repository.update(quotation)

        opportunity.status = OpportunityStatus.WON
        opportunity.converted_customer_id = customer.id
        self.opportunity_repository.update(opportunity)

        return customer

    # ── Auto-expire scheduled job ───────────────────────────────────────
    # Mirrors ERPNext's set_expired_status(). Wire this to the existing
    # scheduler (same mechanism used for Opportunity's auto-close).

    def auto_expire_stale_quotations(self, business_id: uuid.UUID) -> int:
        today = datetime.now(timezone.utc).date()
        expiring = self.repository.list_sent_expiring_before(business_id, today)
        for quotation in expiring:
            quotation.status = QuotationStatus.EXPIRED
            self.repository.update(quotation)
        return len(expiring)
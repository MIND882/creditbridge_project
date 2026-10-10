"""Pydantic v2 schemas for PaymentTermsTemplateDetail (child table, read-only API)."""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from app.accounts.payment_term_domain.models.payment_term import DiscountType, DueDateBasedOn

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PaymentTermsTemplateDetailCreate",

    "PaymentTermsTemplateDetailRead",

    "PaymentTermsTemplateDetailListResponse",

]





class PaymentTermsTemplateDetailCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    payment_term_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    invoice_portion: Decimal

    due_date_based_on: DueDateBasedOn

    credit_days: Optional[int] = None

    credit_months: Optional[int] = None

    mode_of_payment: Optional[str] = None

    discount_type: Optional[DiscountType] = DiscountType.PERCENTAGE

    discount: Optional[Decimal] = None

    discount_validity_based_on: Optional[DueDateBasedOn] = None

    discount_validity: Optional[int] = None





class PaymentTermsTemplateDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    payment_term_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    invoice_portion: Optional[Decimal] = None

    due_date_based_on: Optional[DueDateBasedOn] = None

    credit_days: Optional[int] = None

    credit_months: Optional[int] = None

    mode_of_payment: Optional[str] = None

    discount_type: Optional[DiscountType] = None

    discount: Optional[Decimal] = None

    discount_validity_based_on: Optional[DueDateBasedOn] = None

    discount_validity: Optional[int] = None





PaymentTermsTemplateDetailListResponse = Page[PaymentTermsTemplateDetailRead]

"""

Pydantic v2 contracts for Payment Schedule.



An orphan child table: upstream's parents are Sales Invoice and Purchase Invoice,

neither of which is converted. So the API is read-only -- rows appear when an

invoice is posted, and there is no parent here to post them through yet.

"""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal

from typing import Optional



from app.accounts.payment_term_domain.models.payment_term import DiscountType, DueDateBasedOn

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["PaymentScheduleCreate", "PaymentScheduleRead", "PaymentScheduleListResponse"]





class PaymentScheduleCreate(InputSchema):

    """Accepted only nested inside a parent invoice payload, once converted."""



    payment_term_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    due_date: dt.date

    invoice_portion: Optional[Decimal] = None

    payment_amount: Decimal

    mode_of_payment: Optional[str] = None

    paid_amount: Optional[Decimal] = None

    discounted_amount: Optional[Decimal] = None

    outstanding: Optional[Decimal] = None

    discount_date: Optional[dt.date] = None

    discount_type: Optional[DiscountType] = DiscountType.PERCENTAGE

    discount: Optional[Decimal] = None

    base_payment_amount: Optional[Decimal] = None

    base_outstanding: Optional[Decimal] = None

    base_paid_amount: Optional[Decimal] = None

    due_date_based_on: Optional[DueDateBasedOn] = None

    credit_days: Optional[int] = None

    credit_months: Optional[int] = None

    discount_validity_based_on: Optional[DueDateBasedOn] = None

    discount_validity: Optional[int] = None





class PaymentScheduleRead(ReadSchema):

    id: uuid.UUID

    payment_term_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    due_date: Optional[dt.date] = None

    invoice_portion: Optional[Decimal] = None

    payment_amount: Optional[Decimal] = None

    mode_of_payment: Optional[str] = None

    paid_amount: Optional[Decimal] = None

    discounted_amount: Optional[Decimal] = None

    outstanding: Optional[Decimal] = None

    discount_date: Optional[dt.date] = None

    discount_type: Optional[DiscountType] = None

    discount: Optional[Decimal] = None

    base_payment_amount: Optional[Decimal] = None

    base_outstanding: Optional[Decimal] = None

    base_paid_amount: Optional[Decimal] = None

    due_date_based_on: Optional[DueDateBasedOn] = None

    credit_days: Optional[int] = None

    credit_months: Optional[int] = None

    discount_validity_based_on: Optional[DueDateBasedOn] = None

    discount_validity: Optional[int] = None





PaymentScheduleListResponse = Page[PaymentScheduleRead]

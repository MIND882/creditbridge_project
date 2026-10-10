"""

Payment Term -- converted from ``erpnext/accounts/doctype/payment_term``.



One instalment rule: what share of the invoice falls due, how long the customer

gets, and what discount applies if they pay early. Composed into a

Payment Terms Template, which is what an invoice actually points at.



``autoname`` is ``field:payment_term_name``, so ``name`` is that field verbatim.

"""



from __future__ import annotations



import enum

import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel, tenant_index



__all__ = ["PaymentTerm", "DueDateBasedOn", "DiscountType"]





class DueDateBasedOn(str, enum.Enum):

    """Shared by Payment Term, its template detail, and Payment Schedule."""



    DAYS_AFTER_INVOICE_DATE = "Day(s) after invoice date"

    DAYS_AFTER_END_OF_INVOICE_MONTH = "Day(s) after the end of the invoice month"

    MONTHS_AFTER_END_OF_INVOICE_MONTH = "Month(s) after the end of the invoice month"





class DiscountType(str, enum.Enum):

    PERCENTAGE = "Percentage"

    AMOUNT = "Amount"





class PaymentTerm(TenantModel):

    __tablename__ = "payment_terms"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_payment_term_business_name"),

        tenant_index("ix_payment_term_name", "name"),

    )



    #: ``autoname = field:payment_term_name``.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    payment_term_name: Mapped[str] = mapped_column(String(140), nullable=False)



    #: Share of the invoice this term covers, as a percentage.

    invoice_portion: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    #: Mode of Payment is its own doctype and is not converted.

    mode_of_payment: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    due_date_based_on: Mapped[Optional[DueDateBasedOn]] = mapped_column(

        SAEnum(DueDateBasedOn, name="due_date_based_on"), nullable=True

    )

    credit_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    credit_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    discount_type: Mapped[Optional[DiscountType]] = mapped_column(

        SAEnum(DiscountType, name="discount_type"), default=DiscountType.PERCENTAGE, nullable=True

    )

    discount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    discount_validity_based_on: Mapped[Optional[DueDateBasedOn]] = mapped_column(

        SAEnum(DueDateBasedOn, name="discount_validity_based_on"),

        default=DueDateBasedOn.DAYS_AFTER_INVOICE_DATE,

        nullable=True,

    )

    discount_validity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



    def __repr__(self) -> str:

        return f"<PaymentTerm id={self.id} name={self.name!r} portion={self.invoice_portion}>"

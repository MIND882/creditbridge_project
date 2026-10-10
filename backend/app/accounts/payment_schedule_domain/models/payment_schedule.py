"""

PaymentSchedule -- converted from ``erpnext/accounts/doctype/payment_schedule``.



The instalment plan attached to an invoice: one row per term, with the due date,

the amount falling due, and how much of it has been paid.



**Orphan child table.** Upstream's parents are Sales Invoice and Purchase

Invoice, neither of which is converted. So there is no ``parent_id`` FK here --

the rows are tenant-scoped and addressed by ``payment_term`` instead. Wiring a

parent in later means adding the column, not restructuring this model.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.payment_term_domain.models.payment_term import DiscountType, DueDateBasedOn

from app.core.base_model import TenantModel, tenant_index



__all__ = ["PaymentSchedule"]





class PaymentSchedule(TenantModel):

    __tablename__ = "payment_schedules"

    __table_args__ = (tenant_index("ix_payment_schedule_due_date", "due_date"),)



    payment_term_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    payment_term = relationship("PaymentTerm", foreign_keys=[payment_term_id])



    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    due_date: Mapped[date] = mapped_column(Date, nullable=False)



    #: Percent, stored at the same precision as the currency columns.

    invoice_portion: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    payment_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=False)



    #: Mode of Payment is its own doctype and is not converted.

    mode_of_payment: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    paid_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discounted_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), default=0, nullable=True

    )



    #: Derived upstream as payment_amount - paid_amount - discounted_amount.

    outstanding: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    discount_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    discount_type: Mapped[Optional[DiscountType]] = mapped_column(

        SAEnum(DiscountType, name="discount_type"), default=DiscountType.PERCENTAGE, nullable=True

    )

    discount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    # Company-currency copies of the three amounts above.

    base_payment_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_outstanding: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_paid_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    due_date_based_on: Mapped[Optional[DueDateBasedOn]] = mapped_column(

        SAEnum(DueDateBasedOn, name="due_date_based_on"), nullable=True

    )

    credit_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    credit_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



    discount_validity_based_on: Mapped[Optional[DueDateBasedOn]] = mapped_column(

        SAEnum(DueDateBasedOn, name="discount_validity_based_on"), nullable=True

    )

    discount_validity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



    def __repr__(self) -> str:

        return f"<PaymentSchedule id={self.id} due={self.due_date} amount={self.payment_amount}>"

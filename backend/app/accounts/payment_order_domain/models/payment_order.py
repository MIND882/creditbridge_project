"""

Payment Order -- converted from ``erpnext/accounts/doctype/payment_order``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.payment_order_reference_domain.models.payment_order_reference import PaymentOrderReference



from app.accounts.bank_account_domain.models.bank_account import BankAccount  # noqa: F401

from app.accounts.bank_domain.models.bank import Bank  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["PaymentOrder", "PaymentOrderNamingSeries", "PaymentOrderPaymentOrderType"]







class PaymentOrderNamingSeries(str, enum.Enum):

    PMO = "PMO-"





class PaymentOrderPaymentOrderType(str, enum.Enum):

    PAYMENT_REQUEST = "Payment Request"

    PAYMENT_ENTRY = "Payment Entry"









class PaymentOrder(SubmittableModel, TenantModel):

    __tablename__ = "payment_orders"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_payment_orders_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[PaymentOrderNamingSeries] = mapped_column(

        SAEnum(PaymentOrderNamingSeries, native_enum=False, length=4, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_order_type: Mapped[PaymentOrderPaymentOrderType] = mapped_column(

        SAEnum(PaymentOrderPaymentOrderType, native_enum=False, length=15, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    company_bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    company_bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[company_bank_account_id])

    company_bank_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("banks.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    company_bank = relationship("Bank", foreign_keys=[company_bank_id])

    account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    references = relationship(

        PaymentOrderReference,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PaymentOrderReference.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentOrder id={self.id}>"

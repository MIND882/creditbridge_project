"""

Payment Request -- converted from ``erpnext/accounts/doctype/payment_request``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.payment_reference_domain.models.payment_reference import PaymentReference

from app.accounts.subscription_plan_detail_domain.models.subscription_plan_detail import SubscriptionPlanDetail



from app.accounts.bank_account_domain.models.bank_account import BankAccount  # noqa: F401

from app.accounts.bank_domain.models.bank import Bank  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401

from app.accounts.mode_of_payment_domain.models.mode_of_payment import ModeOfPayment  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["PaymentRequest", "PaymentRequestPaymentRequestType", "PaymentRequestNamingSeries", "PaymentRequestStatus", "PaymentRequestPaymentChannel"]







class PaymentRequestPaymentRequestType(str, enum.Enum):

    OUTWARD = "Outward"

    INWARD = "Inward"





class PaymentRequestNamingSeries(str, enum.Enum):

    ACC_PRQ_YYYY = "ACC-PRQ-.YYYY.-"





class PaymentRequestStatus(str, enum.Enum):

    DRAFT = "Draft"

    REQUESTED = "Requested"

    INITIATED = "Initiated"

    PARTIALLY_PAID = "Partially Paid"

    PAYMENT_ORDERED = "Payment Ordered"

    PAID = "Paid"

    FAILED = "Failed"

    CANCELLED = "Cancelled"





class PaymentRequestPaymentChannel(str, enum.Enum):

    EMAIL = "Email"

    PHONE = "Phone"

    OTHER = "Other"









class PaymentRequest(SubmittableModel, TenantModel):

    __tablename__ = "payment_requests"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_payment_requests_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    payment_request_type: Mapped[PaymentRequestPaymentRequestType] = mapped_column(

        SAEnum(PaymentRequestPaymentRequestType, native_enum=False, length=7, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    transaction_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    naming_series: Mapped[PaymentRequestNamingSeries] = mapped_column(

        SAEnum(PaymentRequestNamingSeries, native_enum=False, length=15, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    mode_of_payment_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("mode_of_payments.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    mode_of_payment = relationship("ModeOfPayment", foreign_keys=[mode_of_payment_id])

    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    grand_total: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    is_a_subscription: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[bank_account_id])

    bank_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("banks.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bank = relationship("Bank", foreign_keys=[bank_id])

    bank_account_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    iban: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    branch_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    swift_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    print_format: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    email_to: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    subject: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_gateway_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[Optional[PaymentRequestStatus]] = mapped_column(

        SAEnum(PaymentRequestStatus, native_enum=False, length=15, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    make_sales_invoice: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    mute_email: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    payment_url: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_gateway: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_channel: Mapped[Optional[PaymentRequestPaymentChannel]] = mapped_column(

        SAEnum(PaymentRequestPaymentChannel, native_enum=False, length=5, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    payment_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    failed_reason: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    outstanding_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    party_account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    phone_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    subscription_plans = relationship(

        SubscriptionPlanDetail,

        primaryjoin="and_(PaymentRequest.id == foreign(SubscriptionPlanDetail.parent_id), SubscriptionPlanDetail.parenttype == 'Payment Request')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=SubscriptionPlanDetail.idx,

        overlaps="plans",

    )

    payment_reference = relationship(

        PaymentReference,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PaymentReference.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentRequest id={self.id}>"

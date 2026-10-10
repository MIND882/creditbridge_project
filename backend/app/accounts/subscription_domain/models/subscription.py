"""

Subscription -- converted from ``erpnext/accounts/doctype/subscription``.





"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.subscription_plan_detail_domain.models.subscription_plan_detail import SubscriptionPlanDetail



from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["Subscription", "SubscriptionStatus", "SubscriptionApplyAdditionalDiscount", "SubscriptionGenerateInvoiceAt"]







class SubscriptionStatus(str, enum.Enum):

    TRIALING = "Trialing"

    ACTIVE = "Active"

    GRACE_PERIOD = "Grace Period"

    CANCELLED = "Cancelled"

    UNPAID = "Unpaid"

    COMPLETED = "Completed"

    REFUNDED = "Refunded"





class SubscriptionApplyAdditionalDiscount(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"





class SubscriptionGenerateInvoiceAt(str, enum.Enum):

    POSTPAID_BILL_AT_PERIOD_END = "Postpaid (bill at period end)"

    PREPAID_BILL_AT_PERIOD_START = "Prepaid (bill at period start)"

    BILL_N_DAYS_BEFORE_PERIOD_START = "Bill N days before period start"









class Subscription(TenantModel):

    __tablename__ = "subscriptions"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_subscriptions_business_name"),

    )



    #: ``autoname`` = 'ACC-SUB-.YYYY.-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    status: Mapped[Optional[SubscriptionStatus]] = mapped_column(

        SAEnum(SubscriptionStatus, native_enum=False, length=12, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    cancelation_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    trial_period_start: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    trial_period_end: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    current_invoice_start: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    current_invoice_end: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    next_billing_period_start: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    next_billing_period_end: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    days_until_due: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    apply_additional_discount: Mapped[Optional[SubscriptionApplyAdditionalDiscount]] = mapped_column(

        SAEnum(SubscriptionApplyAdditionalDiscount, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    additional_discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    additional_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_tax_template: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    purchase_tax_template: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    follow_calendar_months: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    generate_new_invoices_past_due_date: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    end_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    start_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    submit_invoice: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    generate_invoice_at: Mapped[SubscriptionGenerateInvoiceAt] = mapped_column(

        SAEnum(SubscriptionGenerateInvoiceAt, native_enum=False, length=31, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    number_of_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



    plans = relationship(

        SubscriptionPlanDetail,

        primaryjoin="and_(Subscription.id == foreign(SubscriptionPlanDetail.parent_id), SubscriptionPlanDetail.parenttype == 'Subscription')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=SubscriptionPlanDetail.idx,

        overlaps="subscription_plans",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Subscription id={self.id}>"

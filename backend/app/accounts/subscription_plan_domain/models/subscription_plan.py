"""

Subscription Plan -- converted from ``erpnext/accounts/doctype/subscription_plan``.





"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["SubscriptionPlan", "SubscriptionPlanPriceDetermination", "SubscriptionPlanBillingInterval"]







class SubscriptionPlanPriceDetermination(str, enum.Enum):

    FIXED_RATE = "Fixed Rate"

    BASED_ON_PRICE_LIST = "Based On Price List"

    MONTHLY_RATE = "Monthly Rate"





class SubscriptionPlanBillingInterval(str, enum.Enum):

    DAY = "Day"

    WEEK = "Week"

    MONTH = "Month"

    YEAR = "Year"









class SubscriptionPlan(TenantModel):

    __tablename__ = "subscription_plans"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_subscription_plans_business_name"),

    )



    #: ``autoname`` = 'field:plan_name'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    plan_name: Mapped[str] = mapped_column(String(140), nullable=False)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    item: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    price_determination: Mapped[SubscriptionPlanPriceDetermination] = mapped_column(

        SAEnum(SubscriptionPlanPriceDetermination, native_enum=False, length=19, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    price_list: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_interval: Mapped[SubscriptionPlanBillingInterval] = mapped_column(

        SAEnum(SubscriptionPlanBillingInterval, native_enum=False, length=5, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    billing_interval_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    payment_gateway: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    product_price_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SubscriptionPlan id={self.id}>"

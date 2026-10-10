"""

Subscription Settings -- converted from ``erpnext/accounts/doctype/subscription_settings``.





"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, Integer, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["SubscriptionSettings"]







class SubscriptionSettings(TenantModel):

    __tablename__ = "subscription_settings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_subscription_settings_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    grace_period: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    cancel_after_grace: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    prorate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SubscriptionSettings id={self.id}>"

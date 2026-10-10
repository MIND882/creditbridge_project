"""

Delivery Settings -- converted from ``erpnext/stock/doctype/delivery_settings``.



A Frappe Single (``issingle: 1``): one row per ``business_id``, enforced by a unique constraint on ``business_id`` alone.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, Integer, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["DeliverySettings"]







class DeliverySettings(TenantModel):

    __tablename__ = "delivery_settingss"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_delivery_settingss_business"),

    )



    dispatch_template: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dispatch_attachment: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    send_with_attachment: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    stop_delay: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<DeliverySettings id={self.id}>"

"""

Customs Tariff Number -- converted from ``erpnext/stock/doctype/customs_tariff_number``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["CustomsTariffNumber"]







class CustomsTariffNumber(TenantModel):

    __tablename__ = "customs_tariff_numbers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_customs_tariff_numbers_business_name"),

    )



    #: ``autoname`` = 'field:tariff_number' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    tariff_number: Mapped[str] = mapped_column(String(140), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CustomsTariffNumber id={self.id}>"

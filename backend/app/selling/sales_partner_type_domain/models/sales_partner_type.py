"""

Sales Partner Type -- converted from ``erpnext/selling/doctype/sales_partner_type``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["SalesPartnerType"]







class SalesPartnerType(TenantModel):

    __tablename__ = "sales_partner_types"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_sales_partner_types_business_name"),

    )



    #: ``autoname`` = 'field:sales_partner_type' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    sales_partner_type: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SalesPartnerType id={self.id}>"

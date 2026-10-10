"""

Industry Type -- converted from ``erpnext/selling/doctype/industry_type``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["IndustryType"]







class IndustryType(TenantModel):

    __tablename__ = "industry_types"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_industry_types_business_name"),

    )



    #: ``autoname`` = 'field:industry' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    industry: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<IndustryType id={self.id}>"

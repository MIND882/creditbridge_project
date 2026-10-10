"""

Brand -- converted from ``erpnext/setup/doctype/brand``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["Brand"]







class Brand(TenantModel):

    __tablename__ = "brands"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_brands_business_name"),

    )



    #: ``autoname`` = 'field:brand' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    brand: Mapped[str] = mapped_column(String(140), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Brand id={self.id}>"

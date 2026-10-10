"""

Manufacturer -- converted from ``erpnext/stock/doctype/manufacturer``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["Manufacturer"]







class Manufacturer(TenantModel):

    __tablename__ = "manufacturers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_manufacturers_business_name"),

    )



    #: ``autoname`` = 'field:short_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    short_name: Mapped[str] = mapped_column(String(140), nullable=False)

    full_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    website: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    country: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    logo: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    notes: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Manufacturer id={self.id}>"

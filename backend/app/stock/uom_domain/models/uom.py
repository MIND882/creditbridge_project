"""

UOM -- converted from ``erpnext/setup/doctype/uom``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["Uom"]







class Uom(TenantModel):

    __tablename__ = "uoms"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_uoms_business_name"),

    )



    #: ``autoname`` = 'field:uom_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    uom_name: Mapped[str] = mapped_column(String(140), nullable=False)

    must_be_whole_number: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    symbol: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    common_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uom_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    category = relationship("UomCategory", foreign_keys=[category_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Uom id={self.id}>"

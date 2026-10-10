"""

UOM Category -- converted from ``erpnext/stock/doctype/uom_category``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["UomCategory"]







class UomCategory(TenantModel):

    __tablename__ = "uom_categories"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_uom_categorys_business_name"),

    )



    #: ``autoname`` = 'field:category_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    category_name: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<UomCategory id={self.id}>"

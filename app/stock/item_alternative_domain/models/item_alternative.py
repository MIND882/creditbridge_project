"""

Item Alternative -- converted from ``erpnext/stock/doctype/item_alternative``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["ItemAlternative"]







class ItemAlternative(TenantModel):

    __tablename__ = "item_alternatives"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_alternatives_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    alternative_item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    alternative_item_code = relationship("Item", foreign_keys=[alternative_item_code_id])

    two_way: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    alternative_item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemAlternative id={self.id}>"

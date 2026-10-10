"""

Item Manufacturer -- converted from ``erpnext/stock/doctype/item_manufacturer``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["ItemManufacturer"]







class ItemManufacturer(TenantModel):

    __tablename__ = "item_manufacturers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_manufacturers_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("manufacturers.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    manufacturer = relationship("Manufacturer", foreign_keys=[manufacturer_id])

    manufacturer_part_no: Mapped[str] = mapped_column(String(140), nullable=False)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemManufacturer id={self.id}>"

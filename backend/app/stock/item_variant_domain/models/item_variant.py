"""

Item Variant -- converted from ``erpnext/stock/doctype/item_variant``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["ItemVariant"]







class ItemVariant(TenantModel):

    __tablename__ = "item_variants"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_variants_business_name"),

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    item_attribute_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_attributes.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_attribute = relationship("ItemAttribute", foreign_keys=[item_attribute_id])

    item_attribute_value: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemVariant id={self.id}>"

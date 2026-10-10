"""

Item Website Specification -- converted from ``erpnext/stock/doctype/item_website_specification``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["ItemWebsiteSpecification"]







class ItemWebsiteSpecification(TenantModel):

    __tablename__ = "item_website_specifications"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_website_specifications_business_name"),

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    label: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemWebsiteSpecification id={self.id}>"

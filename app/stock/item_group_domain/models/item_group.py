"""

Item Group -- converted from ``erpnext/setup/doctype/item_group``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["ItemGroup"]







class ItemGroup(TenantModel):

    __tablename__ = "item_groups"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_groups_business_name"),

    )



    #: ``autoname`` = 'field:item_group_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    item_group_name: Mapped[str] = mapped_column(String(140), nullable=False)

    parent_item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parent_item_group = relationship("ItemGroup", foreign_keys=[parent_item_group_id])

    is_group: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    lft: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    rgt: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    old_parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    old_parent = relationship("ItemGroup", foreign_keys=[old_parent_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemGroup id={self.id}>"

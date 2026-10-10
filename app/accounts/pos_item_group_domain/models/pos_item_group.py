"""

POS Item Group -- converted from ``erpnext/accounts/doctype/pos_item_group``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["POSItemGroup"]







class POSItemGroup(ChildTableModel, TenantModel):

    __tablename__ = "pos_item_groups"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pos_profiles.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("POSProfile", back_populates="item_groups", foreign_keys=[parent_id])



    item_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSItemGroup id={self.id}>"

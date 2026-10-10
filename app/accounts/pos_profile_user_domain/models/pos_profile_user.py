"""

POS Profile User -- converted from ``erpnext/accounts/doctype/pos_profile_user``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["POSProfileUser"]







class POSProfileUser(ChildTableModel, TenantModel):

    __tablename__ = "pos_profile_users"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pos_profiles.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("POSProfile", back_populates="applicable_for_users", foreign_keys=[parent_id])



    default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSProfileUser id={self.id}>"

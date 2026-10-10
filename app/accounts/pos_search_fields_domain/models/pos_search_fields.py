"""

POS Search Fields -- converted from ``erpnext/accounts/doctype/pos_search_fields``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["POSSearchFields"]







class POSSearchFields(ChildTableModel, TenantModel):

    __tablename__ = "pos_search_fields"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pos_settings.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("POSSettings", back_populates="pos_search_fields", foreign_keys=[parent_id])



    fieldname: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    field: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSSearchFields id={self.id}>"

"""

POS Field -- converted from ``erpnext/accounts/doctype/pos_field``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, String, Text, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["POSField"]







class POSField(ChildTableModel, TenantModel):

    __tablename__ = "pos_fields"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pos_settings.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("POSSettings", back_populates="invoice_fields", foreign_keys=[parent_id])



    fieldname: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    fieldtype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    label: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    options: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    reqd: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    read_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    default_value: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSField id={self.id}>"

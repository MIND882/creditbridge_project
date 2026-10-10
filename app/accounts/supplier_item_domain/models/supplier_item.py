"""

Supplier Item -- converted from ``erpnext/accounts/doctype/supplier_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SupplierItem"]







class SupplierItem(ChildTableModel, TenantModel):

    __tablename__ = "supplier_items"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("promotional_schemes.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PromotionalScheme", back_populates="supplier", foreign_keys=[parent_id])



    supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierItem id={self.id}>"

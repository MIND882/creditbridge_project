"""

Customer Item -- converted from ``erpnext/accounts/doctype/customer_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["CustomerItem"]







class CustomerItem(ChildTableModel, TenantModel):

    __tablename__ = "customer_items"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("promotional_schemes.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PromotionalScheme", back_populates="customer", foreign_keys=[parent_id])



    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CustomerItem id={self.id}>"

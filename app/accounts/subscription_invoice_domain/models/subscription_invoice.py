"""

Subscription Invoice -- converted from ``erpnext/accounts/doctype/subscription_invoice``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SubscriptionInvoice"]







class SubscriptionInvoice(ChildTableModel, TenantModel):

    __tablename__ = "subscription_invoices"

    document_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    invoice: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SubscriptionInvoice id={self.id}>"

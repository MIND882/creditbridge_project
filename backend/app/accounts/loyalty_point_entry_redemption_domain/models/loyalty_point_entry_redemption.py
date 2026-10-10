"""

Loyalty Point Entry Redemption -- converted from ``erpnext/accounts/doctype/loyalty_point_entry_redemption``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from typing import Optional

import uuid



from sqlalchemy import Date, Integer, String

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["LoyaltyPointEntryRedemption"]







class LoyaltyPointEntryRedemption(ChildTableModel, TenantModel):

    __tablename__ = "loyalty_point_entry_redemptions"

    sales_invoice: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    redemption_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    redeemed_points: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LoyaltyPointEntryRedemption id={self.id}>"

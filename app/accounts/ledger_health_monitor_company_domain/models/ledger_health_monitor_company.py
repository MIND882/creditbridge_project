"""

Ledger Health Monitor Company -- converted from ``erpnext/accounts/doctype/ledger_health_monitor_company``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["LedgerHealthMonitorCompany"]







class LedgerHealthMonitorCompany(ChildTableModel, TenantModel):

    __tablename__ = "ledger_health_monitor_companies"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("ledger_health_monitors.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("LedgerHealthMonitor", back_populates="companies", foreign_keys=[parent_id])





    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LedgerHealthMonitorCompany id={self.id}>"

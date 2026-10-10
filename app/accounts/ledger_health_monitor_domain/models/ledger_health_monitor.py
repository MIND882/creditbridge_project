"""

Ledger Health Monitor -- converted from ``erpnext/accounts/doctype/ledger_health_monitor``.





"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, Integer, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.ledger_health_monitor_company_domain.models.ledger_health_monitor_company import LedgerHealthMonitorCompany



from app.core.base_model import TenantModel



__all__ = ["LedgerHealthMonitor"]







class LedgerHealthMonitor(TenantModel):

    __tablename__ = "ledger_health_monitors"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_ledger_health_monitors_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    enable_health_monitor: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    debit_credit_mismatch: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    general_and_payment_ledger_mismatch: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    monitor_for_last_x_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)



    companies = relationship(

        LedgerHealthMonitorCompany,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=LedgerHealthMonitorCompany.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LedgerHealthMonitor id={self.id}>"

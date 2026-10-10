"""

Currency Exchange Settings Result -- converted from ``erpnext/accounts/doctype/currency_exchange_settings_result``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["CurrencyExchangeSettingsResult"]







class CurrencyExchangeSettingsResult(ChildTableModel, TenantModel):

    __tablename__ = "currency_exchange_settings_results"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("currency_exchange_settings.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("CurrencyExchangeSettings", back_populates="result_key", foreign_keys=[parent_id])



    key: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CurrencyExchangeSettingsResult id={self.id}>"

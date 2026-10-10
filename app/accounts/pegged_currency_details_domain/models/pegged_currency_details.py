"""

Pegged Currency Details -- converted from ``erpnext/accounts/doctype/pegged_currency_details``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PeggedCurrencyDetails"]







class PeggedCurrencyDetails(ChildTableModel, TenantModel):

    __tablename__ = "pegged_currency_details"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pegged_currencies.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PeggedCurrencies", back_populates="pegged_currency_item", foreign_keys=[parent_id])



    source_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pegged_exchange_rate: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pegged_against: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PeggedCurrencyDetails id={self.id}>"
